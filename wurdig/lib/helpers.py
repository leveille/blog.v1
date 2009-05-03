"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from webhelpers.html import literal
from webhelpers.html.tools import auto_link
from webhelpers.text import truncate, chop_at, plural
from routes import url_for
from wurdig.lib import auth
from wurdig.lib.tag import cloud, post_tags
from wurdig.lib.tidy import *
from wurdig.lib.comment import *
from wurdig.lib.feed_display import *
from webob.exc import strip_tags