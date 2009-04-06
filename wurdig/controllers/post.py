import logging
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import webhelpers.paginate as paginate
import datetime as d
import calendar
import formencode

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from sqlalchemy.sql import and_, delete
from formencode import htmlfill
from wurdig.lib.base import BaseController, render
from authkit.authorize.pylons_adaptors import authorize

log = logging.getLogger(__name__)

class PostController(BaseController):

    def archive(self, year=None, month=None):   
        if year is None:
            abort(404)
        
        (c.posts, c.date, year_i, month_start, month_end, day_end) = (None, year, int(year), 1, 12, 31)
        
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
    
    def new(self):
        # admin
        c.content = 'new'
        return render('/derived/post/new.html')
    
    def create(self):
        # admin
        c.content = 'create'
        # This will ultimately be redirecting
        return render('/derived/post/new.html')
    
    def edit(self, id=None):
        if id is None:
            abort(404)
        # admin
        c.content = 'edit'
        return render('/derived/post/edit.html')
    
    def save(self, id=None):
        # admin
        c.content = 'save'
        # This will ultimately be redirecting
        return render('/derived/post/edit.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        posts_q = meta.Session.query(model.Post).order_by(model.Post.posted_on.desc())
        c.paginator = paginate.Page(
            posts_q.filter(model.Post.posted_on != None),
            page=int(request.params.get('page', 1)),
            items_per_page = 2,
            controller='post',
            action='list',
        )
        return render('/derived/post/list.html')

    def delete(self, id=None):
        if id is None:
            abort(404)
        return render('/derived/post/deleted.html')