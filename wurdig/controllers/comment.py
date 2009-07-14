import datetime
import formencode
import logging
import webhelpers.paginate as paginate
import wurdig.lib.helpers as h
import wurdig.model.meta as meta

from formencode import htmlfill
from pylons import cache, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.cache import beaker_cache
from pylons.decorators.rest import restrict
from pylons.decorators.secure import authenticate_form
from sqlalchemy.sql import and_, delete
from wurdig import model
from wurdig.lib.base import BaseController, render
from wurdig.lib.mail import EmailMessage

log = logging.getLogger(__name__)
    
class AkismetSpamCheck(formencode.FancyValidator):
    messages = {
        'invalid-akismet': 'Your comment has been identified as spam.  Are you a spammer?'
    }
    def _to_python(self, values, state):
        # we're in the administrator
        if request.urlvars['action'] == 'save':
            return values
        
        if h.wurdig_use_akismet():
            from wurdig.lib.akismet import Akismet
            # Thanks for the help from http://soyrex.com/blog/akismet-django-stop-comment-spam/
            a = Akismet(h.wurdig_get_akismet_key(), wurdig_url=request.server_name)
            akismet_data = {}
            akismet_data['user_ip'] = request.remote_addr
            akismet_data['user_agent'] = request.user_agent
            akismet_data['comment_author'] = values['name']
            akismet_data['comment_author_email'] = values['email']
            akismet_data['comment_author_url'] = values['url']
            akismet_data['comment_type'] = 'comment'
            spam = a.comment_check(values['content'], akismet_data)
            if spam:
                raise formencode.Invalid(
                    self.message('invalid-akismet', state),
                    values, state
                )
        return values
    
class PrimitiveSpamCheck(formencode.FancyValidator):
    def _to_python(self, value, state):        
        # Ensure we have a valid string
        value = formencode.validators.UnicodeString(max=10).to_python(value, state)
        eq = h.wurdig_spamword().lower() == value.lower()
        if not eq:
            raise formencode.Invalid("Double check your answer to the spam prevention question and resubmit.", value, state)
        return value

class NewCommentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.validators.UnicodeString(not_empty=True, max=100, strip=True)
    email = formencode.validators.Email(not_empty=True, max=50, strip=True)
    url = formencode.validators.URL(not_empty=False, check_exists=True, max=125, strip=True)
    content = formencode.validators.UnicodeString(
        not_empty=True,
        strip=True,
        messages={
            'empty':'Please enter a comment.'
        }
    )
    approved = formencode.validators.StringBool(if_missing=False)
    
    if not h.auth.authorized(h.auth.is_valid_user):
        rememberme = formencode.validators.StringBool(if_missing=False)
        if h.wurdig_use_akismet():
            chained_validators = [AkismetSpamCheck()]
        else:
            wurdig_comment_question = PrimitiveSpamCheck(not_empty=True, max=10, strip=True)

class CommentController(BaseController):
    
    def new(self, action, post_id=None):
        if post_id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter_by(id=int(post_id)).first() or None
        if c.post is None:
            abort(404)
        return h.comment_form('/derived/comment/new.html')
            
    @restrict('POST')
    @authenticate_form
    @validate(schema=NewCommentForm(), form='new')
    def create(self, action, post_id=None):
        if post_id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter_by(id=int(post_id)).first() or None
        if c.post is None:
            abort(404)
        
        rememberme = None
        if hasattr(self.form_result, 'rememberme'):
            rememberme = self.form_result['rememberme']
            del self.form_result['rememberme']
        if hasattr(self.form_result, 'wurdig_comment_question'):
            del self.form_result['wurdig_comment_question']

        
        comment = model.Comment()
        for k, v in self.form_result.items():
            setattr(comment, k, v)
        comment.post_id = c.post.id

        comment.created_on = datetime.datetime.now()

        comment.content = h.nl2br(comment.content)
        comment.content = h.mytidy(comment.content)
        comment.content = h.comment_filter(comment.content)
        comment.content = h.auto_link(comment.content)
        
        if h.auth.authorized(h.auth.is_valid_user):
            comment.approved = True
            session['flash'] = 'Your comment has been approved.'
        else:
            session['flash'] = 'Your comment is currently being moderated.'
        
        if rememberme is not None:
            h.set_rememberme_cookie(rememberme, comment)
        
        session.save()
        meta.Session.add(comment)
        meta.Session.commit()
        
        if not h.auth.authorized(h.auth.is_valid_user):
            # Send email to admin notifying of new comment
            c.comment = comment
            message = EmailMessage(subject='New Comment for "%s"' % c.post.title,
                                   body=render('/email/new_comment.html'),
                                   from_email='%s <%s>' % (comment.name, comment.email),
                                   to=[h.wurdig_contact_email()])
            message.send(fail_silently=True)
                
        return redirect_to(controller='post', 
                           action='view', 
                           year=c.post.posted_on.strftime('%Y'),
                           month=c.post.posted_on.strftime('%m'),
                           slug=c.post.slug
                           )

    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        values = {
            'name': comment.name,
            'email': comment.email,
            'url': comment.url,
            'content': comment.content,
            'approved' : comment.approved
        }
        return htmlfill.render(render('/derived/comment/edit.html'), values)

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewCommentForm(), form='edit')
    def save(self, id=None):
        if id is None:
            abort(404)
            
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        
        if comment is None:
            abort(404)
            
        if hasattr(self.form_result, 'rememberme'):
            del self.form_result['rememberme']
            
        if hasattr(self.form_result, 'wurdig_comment_question'):
            del self.form_result['wurdig_comment_question']
            
        for k,v in self.form_result.items():
            if getattr(comment, k) != v:
                setattr(comment, k, v)
        
        comment.content = h.mytidy(comment.content)
        comment.content = h.auto_link(comment.content)
        
        meta.Session.commit()
        session['flash'] = 'Comment successfully updated.'
        session.save()
        return redirect_to(controller='comment', action='list')

    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        comments_q = meta.Session.query(model.Comment).order_by(
                                                   model.Comment.approved
                                                   ).order_by(model.Comment.created_on.desc())
        comments_q = comments_q.all()
        c.paginator = paginate.Page(
            comments_q,
            page=int(request.params.get('page', 1)),
            items_per_page=20,
            controller='comment',
            action='list'
        )
        return render('/derived/comment/list.html')
     
    """
    @todo: Way too much redundancy below.  This needs to be refactored ... DRY 
    """
    
    @h.auth.authorize(h.auth.is_valid_user)
    def approve_confirm(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        c.comment = comment_q.filter_by(id=id).first()
        if c.comment is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = c.comment.post_id and post_q.filter_by(id=int(c.comment.post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/approve_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def approve(self, id=None):
        id = request.params.getone('id')
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        comment.approved=True
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The comment has been approved'}"
        else:
            session['flash'] = 'Comment successfully approved.'
            session.save()
            return redirect_to(controller='comment', action='list')
            
    @h.auth.authorize(h.auth.is_valid_user)
    def disapprove_confirm(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        c.comment = comment_q.filter_by(id=id).first()
        if c.comment is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = c.comment.post_id and post_q.filter_by(id=int(c.comment.post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/disapprove_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def disapprove(self, id=None):
        id = request.params.getone('id')
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        comment.approved=False
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The comment has been approved'}"
        else:
            session['flash'] = 'Comment successfully approved.'
            session.save()
            return redirect_to(controller='comment', action='list')

    @h.auth.authorize(h.auth.is_valid_user)
    def delete_confirm(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        c.comment = comment_q.filter_by(id=id).first()
        if c.comment is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = c.comment.post_id and post_q.filter_by(id=int(c.comment.post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/delete_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):
        id = request.params.getone('id')
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        meta.Session.delete(comment)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The comment has been deleted'}"
        else:
            session['flash'] = 'Comment successfully deleted.'
            session.save()
            return redirect_to(controller='comment', action='list')
