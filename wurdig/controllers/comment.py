import logging
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import formencode
import webhelpers.paginate as paginate

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from wurdig import model
from wurdig.lib.base import BaseController, render
from formencode import htmlfill
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from pylons.decorators.secure import authenticate_form
from webhelpers.html.converters import markdown
from wurdig.lib.akismet import Akismet

log = logging.getLogger(__name__)
    
class SpamCheck(formencode.FancyValidator):
    messages = {
        'invalid': 'Your comment has been identified as spam.  Please modify your comment.'
    }
    def _to_python(self, values, state):
        # we're in the administrator
        if request.urlvars['action'] == 'save':
            return values
        
        from pylons import config
        # Thanks for the help from http://soyrex.com/blog/akismet-django-stop-comment-spam/
        a = Akismet(config['akismet.api_key'], blog_url=request.server_name)
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
                self.message('invalid', state),
                values, state
            )
        return values

class NewCommentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.validators.UnicodeString(not_empty=True, max=100)
    email = formencode.validators.Email(not_empty=True, max=50)
    url = formencode.validators.URL(not_empty=False, check_exists=True, max=125)
    content = formencode.validators.UnicodeString(
        not_empty=True,
        messages={
            'empty':'Please enter a comment.'
        }
    )
    approved = formencode.validators.StringBool(if_missing=False)
    chained_validators = [SpamCheck()]

class CommentController(BaseController):

    def new(self, action, post_id=None):
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter_by(id=int(post_id)).first() or None
        if c.post is None:
            abort(404)
        return render('/derived/comment/new.html')
    
    @restrict('POST')
    @authenticate_form
    @validate(schema=NewCommentForm(), form='new')
    def create(self, action, post_id=None):
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter_by(id=int(post_id)).first() or None
        if c.post is None:
            abort(404)
        comment = model.Comment()
        for k, v in self.form_result.items():
            setattr(comment, k, v)
        comment.post_id = c.post.id
        comment.content = markdown(comment.content, safe_mode="remove")        
        meta.Session.add(comment)
        meta.Session.commit()
        # @todo: email administrator w/ each new comment
        session['flash'] = 'Your comment is currently being moderated.'
        session.save()
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
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        for k,v in self.form_result.items():
            if getattr(comment, k) != v:
                setattr(comment, k, v)
        meta.Session.commit()
        session['flash'] = 'Comment successfully updated.'
        session.save()
        return redirect_to(controller='comment', action='list')

    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        comments_q = meta.Session.query(model.Comment).order_by(
                                                   model.Comment.approved
                                                   ).order_by(model.Comment.created_on)
        comments_q = comments_q.all()
        c.paginator = paginate.Page(
            comments_q,
            page=int(request.params.get('page', 1)),
            items_per_page=20,
            controller='comment',
            action='list'
        )
        return render('/derived/comment/list.html')

    @h.auth.authorize(h.auth.is_valid_user)
    def delete(self, id=None):
        if id is None:
            abort(404)
        comment_q = meta.Session.query(model.Comment)
        comment = comment_q.filter_by(id=id).first()
        if comment is None:
            abort(404)
        meta.Session.delete(comment)
        meta.Session.commit()
        session['flash'] = 'Comment successfully deleted.'
        session.save()
        return redirect_to(controller='comment', action='list')
