"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from routes import url_for
from webhelpers.html import literal
from webhelpers.html.secure_form import secure_form
from webhelpers.html.tags import *
from webhelpers.html.tools import auto_link, mail_to
from webhelpers.text import truncate, chop_at, plural
from webob.exc import strip_tags

from wurdig.lib import auth
from wurdig.lib.comment import *
from wurdig.lib.conf_helper import *
from wurdig.lib.feed_display import *
from wurdig.lib.html import *
from wurdig.lib.mdown import *
from wurdig.lib.tag import cloud, post_tags
from wurdig.lib.tidy_helper import *
from wurdig.lib.utils_helper import *

def load_stylesheet_assets(csslist='FCSSLIST'):
    import pylons
    import os
    path = os.path.join(pylons.config['pylons.paths']['static_files'], 'css',
                        '%s')
    f = open(path % csslist,'r')
    stylesheets = f.read()
    f.close()
    return ['/css/%s.css?%s' % (f, mtime('/css/%s.css' % f)) for f in stylesheets.split()]