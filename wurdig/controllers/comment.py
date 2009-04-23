import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from wurdig.lib.base import BaseController, render
from wurdig import model

import wurdig.model.meta as meta
import wurdig.lib.helpers as h

import formencode
from formencode import htmlfill
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from pylons.decorators.secure import authenticate_form
import webhelpers.paginate as paginate

log = logging.getLogger(__name__)

class NewCommentForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.validators.String(not_empty=True, max=100)
    email = formencode.validators.Email(not_empty=True, max=50)
    url = formencode.validators.URL(not_empty=False, check_exists=True, max=125)
    content = formencode.validators.String(
        not_empty=True,
        messages={
            'empty':'Please enter a comment.'
        }
    )
    approved = formencode.validators.StringBool(if_missing=False)

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
        meta.Session.add(comment)
        meta.Session.commit()
        # @todo: email administrator w/ each new comment
        return redirect_to(controller='post', 
                           action='view', 
                           year=c.post.posted_on.strftime('%Y'),
                           month=c.post.posted_on.strftime('%m'),
                           slug=c.post.slug,
                           state='comment_moderated'
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
