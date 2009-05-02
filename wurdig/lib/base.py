"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from pylons import config, tmpl_context as c
from wurdig import model
from wurdig.model import meta
from wurdig.lib import feedparser

class BaseController(WSGIController):

    def __before__(self, action, pageid=None):
        # grab tag list and x recent comments for display in sidebar
        tags_q = meta.Session.query(model.Tag)
        c.tags = tags_q.all()
        
        comments_q = meta.Session.query(model.Comment).filter(model.Comment.approved==True)
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc())
        c.recent_comments = comments_q.join(model.Post).limit(5)
        
        c.twitter_feed = feedparser.parse("http://twitter.com/statuses/user_timeline/%s.rss" % config['twitter.user.screen_name'])
        c.delicious_feed = feedparser.parse('http://feeds.delicious.com/v2/rss/%s?count=10' % config['delicious.username']) 
        c.flickr_feed = feedparser.parse('http://api.flickr.com/services/feeds/photos_public.gne?id=%s@N00&lang=en-us&format=rss_200' % config['flickr.id'])
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
