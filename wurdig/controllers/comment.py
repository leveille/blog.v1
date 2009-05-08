import formencode
import logging
import wurdig.lib.helpers as h
import wurdig.model.meta as meta
import webhelpers.paginate as paginate

from formencode import htmlfill
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from pylons.decorators.secure import authenticate_form
from sqlalchemy.sql import and_, delete
from webhelpers.feedgenerator import Atom1Feed
from wurdig import model
from wurdig.lib.base import BaseController, render

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
        eq = h.wurdig_spamword() == value.lower()
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
    
    if h.wurdig_use_akismet():
        chained_validators = [AkismetSpamCheck()]
    else:
        wurdig_comment_question = PrimitiveSpamCheck(not_empty=True, max=10, strip=True)

class CommentController(BaseController):
        
    def list(self):
        comments_q = meta.Session.query(model.Comment).filter_by(pageid=c.page.id)
        comments_q = comments_q.order_by(model.comment_table.c.created.asc())
        c.paginator = paginate.Page(
            comments_q,
            page=int(request.params.get('page', 1)),
            items_per_page=10,
            pageid=c.pageid,
            controller='comment',
            action='list'
        )
        return render('/derived/comment/list.html')
    
    def feeds(self):  
                
        comments_q = meta.Session.query(model.Comment).filter(model.Comment.approved==True)
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(20)
        
        feed = Atom1Feed(
            title=u"Comments for " + h.wurdig_title(),
            subtitle=h.wurdig_subtitle(),
            link=u"http://%s" % request.server_name,
            description=h.wurdig_subtitle(),
            language=u"en",
        )
        
        for comment in comments_q:
            post_q = meta.Session.query(model.Post)
            c.post = comment.post_id and post_q.filter_by(id=int(comment.post_id)).first() or None
            if c.post is not None:
                feed.add_item(
                    title=u"Comment on %s" % c.post.title,
                    link=h.url_for(
                        controller='post', 
                        action='view', 
                        year=c.post.posted_on.strftime('%Y'), 
                        month=c.post.posted_on.strftime('%m'), 
                        slug=c.post.slug,
                        anchor=u"comment-" + str(comment.id)
                    ),
                    description=comment.content
                )
                
        response.content_type = u'application/atom+xml'
        return feed.writeString('utf-8')
    
    def post_comment_feed(self, post_id=None):
        if post_id is None:
            abort(404)
        
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter(and_(model.Post.id==int(post_id), 
                                                model.Post.draft==False)).first() or None
        if c.post is None:
            abort(404)
        comments_q = meta.Session.query(model.Comment).filter(and_(model.Comment.post_id==c.post.id, 
                                                                   model.Comment.approved==True))
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(10)
        
        feed = Atom1Feed(
            title=h.wurdig_title() + u' - ' + c.post.title,
            subtitle=u'Most Recent Comments',
            link=h.url_for(
                    controller='post', 
                    action='view', 
                    year=c.post.posted_on.strftime('%Y'), 
                    month=c.post.posted_on.strftime('%m'), 
                    slug=c.post.slug
                ),
            description=u"Most recent comments for %s" % c.post.title,
            language=u"en",
        )
        
        for comment in comments_q:
            feed.add_item(
                title=c.post.title + u" comment #%s" % comment.id,
                link=h.url_for(
                    controller='post', 
                    action='view', 
                    year=c.post.posted_on.strftime('%Y'), 
                    month=c.post.posted_on.strftime('%m'), 
                    slug=c.post.slug,
                    anchor=u"comment-" + str(comment.id)
                ),
                description=comment.content
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
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
        if self.form_result['wurdig_comment_question'] is not None:
            del self.form_result['wurdig_comment_question']
        comment = model.Comment()
        for k, v in self.form_result.items():
            setattr(comment, k, v)
        comment.post_id = c.post.id

        comment.content = h.tidy(comment.content)
        comment.content = h.comment_filter(comment.content)
        
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
        if self.form_result['wurdig_comment_question'] is not None:
            del self.form_result['wurdig_comment_question']
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