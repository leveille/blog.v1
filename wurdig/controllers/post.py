import logging
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import webhelpers.paginate as paginate
import datetime as d
import calendar
import formencode
import re

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from sqlalchemy.sql import and_, delete
from formencode import htmlfill
from wurdig.lib.base import BaseController, render
from authkit.authorize.pylons_adaptors import authorize

log = logging.getLogger(__name__)

class ConstructSlug(formencode.FancyValidator):
    def _to_python(self, value, state):
        if value['slug'] in ['', u'', None]:
            post_title = value['title'].lower()
            value['slug'] = re.compile(r'[^\w-]+', re.U).sub('-', post_title).strip('-')
        return value

class UniquePostSlug(formencode.FancyValidator):
    messages = {
        'invalid': 'Slug must be unique'
    }
    def _to_python(self, value, state):
        if value.has_key('id') and value['id'] is not None:
            # we're editing an existing post.
            query = meta.Session.query(model.Post)
            item = query.filter(and_(model.Post.id!=value['id'], 
                                     model.Post.slug==value['slug'])).first()
        else:
            # we're adding a new post.
            query = meta.Session.query(model.Post)
            item = query.filter(model.Post.slug==value['slug']).first()
            
        if item:
            raise formencode.Invalid(
                self.message('invalid', state),
                value, state)
        
        return value

class NewPostForm(formencode.Schema):
    pre_validators = [ConstructSlug()]
    allow_extra_fields = True
    filter_extra_fields = True
    title = formencode.validators.UnicodeString(
        not_empty=True,
        messages={
            'empty':'Enter a post title'
        },
        strip=True
    )
    slug = formencode.validators.UnicodeString(max=30, strip=True)
    content = formencode.validators.UnicodeString(
        not_empty=True,
        messages={
            'empty':'Enter some post content.'
        },
        strip=True
    )
    draft = formencode.validators.StringBool(if_missing=False)
    comments_allowed = formencode.validators.StringBool(if_missing=False)
    chained_validators = [UniquePostSlug()]
    
class EditPostForm(NewPostForm):
    id = formencode.validators.Int()

class PostController(BaseController):
    # @todo: Assign tags to posts for add/edit
    # @todo: Enable commenting for posts
    # @todo: Need to figure out why check="checked" is not working
    # for edit post
    def archive(self, year=None, month=None):   
        if year is None:
            abort(404)
        
        (c.date, year_i, month_start, month_end, day_end) = (year, int(year), 1, 12, 31)
        
        if month is not None:
            c.date = calendar.month_name[month_start] + ', ' + year
            (month_start, month_end) = (int(month), int(month))
            day_end = calendar.monthrange(year_i, month_start)[1]
            
        posts_q = meta.Session.query(model.Post).order_by(model.Post.posted_on.desc())

        c.paginator = paginate.Page(
            posts_q.filter(and_(model.Post.posted_on >= d.datetime(year_i, month_start, 1), 
                model.Post.posted_on <= d.datetime(year_i, month_end, day_end))
            ),
            page=int(request.params.get('page', 1)),
            items_per_page = 1,
            controller='post',
            action='archive',
            year=year,
            month=month,
        )
                
        return render('/derived/post/archive.html')
    
    def view(self, year, month, slug):
        (year_i, month_i) = (int(year), int(month))
        c.post = meta.Session.query(model.Post).filter(
            and_(model.Post.posted_on >= d.datetime(year_i, month_i, 1), 
                 model.Post.posted_on <= d.datetime(year_i, month_i, calendar.monthrange(year_i, month_i)[1]),
                 model.Post.slug == slug)
        ).first()
                                 
        if c.post is None:
            abort(404)
        c.post.content = h.literal(c.post.content)
        return render('/derived/post/view.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def new(self):
        return render('/derived/post/new.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewPostForm(), form='new')
    def create(self):
        post = model.Post()
        
        for k, v in self.form_result.items():
            setattr(post, k, v)
        
        if post.draft in [None, False]:
            post.posted_on = d.datetime.now()
            
        meta.Session.add(post)
        meta.Session.commit()
        session['flash'] = 'Post successfully added.'
        session.save()
        # Issue an HTTP redirect
        if post.posted_on is not None:
            return redirect_to(controller='post', 
                               action='view', 
                               year=post.posted_on.strftime('%Y'), 
                               month=post.posted_on.strftime('%m'), 
                               slug=post.slug)
        else:
            return redirect_to(controller='post', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
        values = {
            'id':post.id,
            'title':post.title,
            'slug':post.slug,
            'content':post.content,
            'draft':post.posted_on is None,
            'comments_allowed':post.comments_allowed
        }
        return htmlfill.render(render('/derived/post/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=EditPostForm(), form='edit')
    def save(self, id=None):
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
            
        for k,v in self.form_result.items():
            if getattr(post, k) != v:
                setattr(post, k, v)
         
        if post.draft:
            post.posted_on = None
            
        meta.Session.commit()
        session['flash'] = 'Post successfully updated.'
        session.save()

        if post.posted_on is not None:
            return redirect_to(controller='post', 
                               action='view', 
                               year=post.posted_on.strftime('%Y'), 
                               month=post.posted_on.strftime('%m'), 
                               slug=post.slug)
        else:
            return redirect_to(controller='post', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        posts_q = meta.Session.query(model.Post).order_by(model.Post.created_on.desc())
        c.paginator = paginate.Page(
            posts_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='post',
            action='list',
        )
        return render('/derived/post/list.html')

    @h.auth.authorize(h.auth.is_valid_user)
    def delete(self, id=None):
        # @todo: delete confirmation
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
        meta.Session.execute(delete(model.poststags_table, model.poststags_table.c.post_id==post.id))
        meta.Session.delete(post)
        meta.Session.commit()
        session['flash'] = 'Post successfully deleted.'
        session.save()
        return redirect_to(controller='post', action='list')