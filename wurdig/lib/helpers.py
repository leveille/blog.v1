"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form
from webhelpers.html import literal
from webhelpers.text import truncate, chop_at, plural
from routes import url_for
from wurdig.lib import auth
from webob.exc import strip_tags