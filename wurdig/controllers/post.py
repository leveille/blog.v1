import logging
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import webhelpers.paginate as paginate
import datetime
import calendar

from sqlalchemy.sql import and_
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PostController(BaseController):

    def archive(self, year=None, month=None):
        """
        Display archived blog posts for a given year,
        or a give year and month
        """
        
        if year is None:
            abort(404)
            
        c.posts = None
        year_i = int(year)
        if month is None:
            c.posts = meta.Session.query(model.Post).filter(
                            and_(model.Post.created_on >= datetime.datetime(year_i, 1, 1), 
                                 model.Post.created_on <= datetime.datetime(year_i, 12, 31),
                                 model.Post.posted_on != None)).all()
        else:
            month_i = int(month)
            month_last_day = calendar.monthrange(year_i, month_i)[1]
            c.posts = meta.Session.query(model.Post).filter(
                            and_(model.Post.created_on >= datetime.datetime(year_i, month_i, 1), 
                                 model.Post.created_on <= datetime.datetime(year_i, month_i, month_last_day),
                                 model.Post.posted_on != None)).all()
        
        c.paginator = paginate.Page(
            c.posts,
            post=int(request.params.get('post', 1)),
            items_per_page = 10,
            controller='post',
            action='archive',
        )
                
        return render('/derived/post/archive.html')
    
    def view(self, year, month, slug=None):
        """
        Display a specific blog post
        """
        if slug is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_q.filter_by(slug=slug).first()
        if c.post is None:
            abort(404)
        c.post.content = h.literal(c.post.content)
        return render('/derived/post/view.html')
