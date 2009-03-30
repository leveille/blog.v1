"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from webhelpers.html.tags import text, textarea, select, submit, password
from routes import url_for
from webhelpers.html.tags import stylesheet_link, javascript_link
from webhelpers.html.tags import link_to
from webhelpers.html import literal
