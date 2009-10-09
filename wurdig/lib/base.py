"""The base Controller API

Provides the BaseController class for subclassing.
"""
import formencode
import helpers as h
import pylons
import re

from paste.deploy.converters import asbool
from pylons import app_globals
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
from wurdig import model
from wurdig.model import meta

class Cleanup(formencode.FancyValidator):
    def _to_python(self, value, state):
        if value['content'] not in ['', u'', None]:
            value['content'] = h.mytidy(value['content'])
        return value
    
class ConstructSlug(formencode.FancyValidator):
    def _to_python(self, value, state):
        if value['slug'] in ['', u'', None]:
            title = value['title'].lower()
            value['slug'] = re.compile(r'[^\w-]+', re.U).sub('-', title).strip('-')
        return value

class BaseController(WSGIController):  
      
    def _setup(self):
        
        def get_db_settings(): 
            return meta.Session.query(model.Setting).all()
        
        # set settings cache object
        # Fails when I attempt to store this in type file
        settings = app_globals.cache.get_cache(
            'base._setup', 
            type='memory'
        ).get(key='settings', createfunc=get_db_settings)
        
        pylons.c.settings = {}
        for setting in settings:
            pylons.c.settings[setting.key] = setting.value    

        pylons.c.display_tagline = asbool(pylons.c.settings.get('display_tagline', 'false'))
        pylons.c.display_admin_email = asbool(pylons.c.settings.get('display_admin_email', 'false'))
        pylons.c.enable_googlesearch = asbool(pylons.c.settings.get('enable_googlesearch', 'false'))
        pylons.c.enable_googleanalytics = asbool(pylons.c.settings.get('enable_googleanalytics', 'false'))
        pylons.c.enable_akismet = asbool(pylons.c.settings.get('enable_akismet', 'false'))
        pylons.c.enable_twitter_display = asbool(pylons.c.settings.get('enable_twitter_display', 'false'))
        pylons.c.enable_delicious_display = asbool(pylons.c.settings.get('enable_delicious_display', 'false'))
        pylons.c.enable_flickr_display = asbool(pylons.c.settings.get('enable_flickr_display', 'false'))
        
        # This is a temporary solution until I find the time to add these settings to the database
        pylons.c.enable_github_display = True
        pylons.c.settings['github_screenname'] = u'leveille'
        
        pylons.c.use_minified_assets = asbool(pylons.c.settings.get('use_minified_assets', 'false'))
        pylons.c.use_externalposts_feed = asbool(pylons.c.settings.get('use_externalposts_feed', 'false'))  
            
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            self._setup()
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()