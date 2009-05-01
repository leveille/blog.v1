"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import tmpl_context as c
from wurdig import model
from wurdig.model import meta

class BaseController(WSGIController):

    def __before__(self, action, pageid=None):
        # grab tag list and x recent comments for display in sidebar
        tags_q = meta.Session.query(model.Tag)
        c.tags = tags_q.all()
        
        comments_q = meta.Session.query(model.Comment).filter(model.Comment.approved==True)
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc())
        c.recent_comments = comments_q.join(model.Post).limit(5)
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
