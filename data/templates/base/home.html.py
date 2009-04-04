from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1238878999.320184
_template_filename='/home/leveille/development/python/pylons/Wurdig/wurdig/templates/base/home.html'
_template_uri='/base/home.html'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['footer', 'secondary_content', 'flash', 'development_stream', 'title', 'tags', 'primary_nav', 'header', 'recent_comments', 'twitter_updates', 'css', 'js', 'categories', 'archives']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">\n<html>\n    <head>\n        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">        \n        <meta http-equiv="Content-Language" content="en-us">\n        <meta name="author" content="Jason R. Leveille">\n        <meta name="copyright" content="http://jasonleveille.com">\n        <link rel="shortcut icon" href="favicon.ico" type="image/x-icon">\n        <meta name="ICBM" content="37.0625, -95.677068">\n        <meta name="geo.position" content="37.0625, -95.677068">\n        <meta name="geo.placename" content="Frederick, Maryland">\n        <meta name="geo.region" content="US-MD">\n        <meta name="geo.country" content="US">\n        \n        <title>')
        # SOURCE LINE 17
        __M_writer(escape(self.title()))
        __M_writer(u'</title>\n        ')
        # SOURCE LINE 18
        __M_writer(escape(self.css()))
        __M_writer(u'\n    </head>\n    \n    <body id="home">\n        \n        <div class="container_16">\n            ')
        # SOURCE LINE 24
        __M_writer(escape(self.primary_nav()))
        __M_writer(u'\n        </div>\n        \n        ')
        # SOURCE LINE 27
        __M_writer(escape(self.header()))
        __M_writer(u'\n        \n        <div id="content">\n            <div class="container_16">\n                \n                <div id="primary-content" class="grid_8">\n                    ')
        # SOURCE LINE 33
        __M_writer(escape(self.flash()))
        __M_writer(u'\n                    ')
        # SOURCE LINE 34
        __M_writer(escape(next.body()))
        __M_writer(u'                    \n                </div>\n                \n                <div id="sidebar" class="grid_8">\n                    <div id="twitter-updates">\n                        ')
        # SOURCE LINE 39
        __M_writer(escape(self.twitter_updates()))
        __M_writer(u'\n                    </div>\n                    <div id="categories" class="grid_4 alpha">\n                        ')
        # SOURCE LINE 42
        __M_writer(escape(self.categories()))
        __M_writer(u'\n                    </div>\n                    <div id="archives" class="grid_4 omega">\n                        ')
        # SOURCE LINE 45
        __M_writer(escape(self.archives()))
        __M_writer(u'\n                    </div>\n                    <div id="tags" class="grid_4 alpha">\n                        ')
        # SOURCE LINE 48
        __M_writer(escape(self.tags()))
        __M_writer(u'\n                    </div>\n                    <div id="recent-comments" class="grid_4 omega">\n                        ')
        # SOURCE LINE 51
        __M_writer(escape(self.recent_comments()))
        __M_writer(u'\n                    </div> \n                    <div id="development-stream">\n                        ')
        # SOURCE LINE 54
        __M_writer(escape(self.development_stream()))
        __M_writer(u'\n                    </div>\n                </div>\n            </div>\n        </div>\n        ')
        # SOURCE LINE 59
        __M_writer(escape(self.secondary_content()))
        __M_writer(u'\n        ')
        # SOURCE LINE 60
        __M_writer(escape(self.footer()))
        __M_writer(u'\n        ')
        # SOURCE LINE 61
        __M_writer(escape(self.js()))
        __M_writer(u'      \n    </body>\n</html>\n\n')
        # SOURCE LINE 65
        __M_writer(u'\n\n')
        # SOURCE LINE 73
        __M_writer(u'\n\n')
        # SOURCE LINE 94
        __M_writer(u'\n\n')
        # SOURCE LINE 119
        __M_writer(u'\n\n')
        # SOURCE LINE 129
        __M_writer(u'\n\n')
        # SOURCE LINE 139
        __M_writer(u'\n\n')
        # SOURCE LINE 149
        __M_writer(u'\n\n')
        # SOURCE LINE 159
        __M_writer(u'\n\n')
        # SOURCE LINE 169
        __M_writer(u'\n\n')
        # SOURCE LINE 179
        __M_writer(u'\n\n')
        # SOURCE LINE 205
        __M_writer(u'\n\n')
        # SOURCE LINE 220
        __M_writer(u'\n\n')
        # SOURCE LINE 230
        __M_writer(u'\n\n')
        # SOURCE LINE 241
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 207
        __M_writer(u'\n    <div id="footer">\n        <div class="container_12">\n            <div class="grid_12">\n                <div class="grid_6 alpha">\n                    <p>Content</p>\n                </div>\n                <div class="grid_6 omega">\n                    <p>Content</p>\n                </div>\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_secondary_content(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 181
        __M_writer(u'\n    <div id="secondary-content">\n        <div class="container_12">\n            <div class=grid_12>\n                <div id="delicious-bookmarks" class="grid_4 alpha">\n                    <h4>Bookmarks</h4>\n                    <ul>\n                        <li>Bookmark</li>\n                        <li>Bookmark</li>\n                        <li>Bookmark</li>\n                        <li>Bookmark</li>\n                    </ul>\n                </div>\n                <div id="flickr-stream" class="grid_4">\n                    <h4>Public Flickr Stream</h4>\n                    <p>Content</p>\n                </div>\n                <div id="blogroll" class="grid_4 omega">\n                    <h4>Blogroll</h4>\n                    <p>Content</p>\n                </div>\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_flash(context):
    context.caller_stack._push_frame()
    try:
        session = context.get('session', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 222
        __M_writer(u'\n')
        # SOURCE LINE 223
        if session.has_key('flash'):
            # SOURCE LINE 224
            __M_writer(u'    <div id="flash"><p>')
            __M_writer(escape(session.get('flash')))
            __M_writer(u'</p></div>\n    ')
            # SOURCE LINE 225

            del session['flash']
            session.save()
                
            
            # SOURCE LINE 228
            __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_development_stream(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 171
        __M_writer(u'\n    <h4>Development Stream</h4>\n    <ul>\n        <li>Link</li>\n        <li>Link</li>\n        <li>Link</li>\n        <li>Link</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 65
        __M_writer(u"Jason Leveille's Blog")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 151
        __M_writer(u'\n    <h4>Tags</h4>\n    <ul>\n        <li>Tag</li>\n        <li>Tag</li>\n        <li>Tag</li>\n        <li>Tag</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_primary_nav(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 96
        __M_writer(u'\n    <div id="primary-nav" class="grid_16">\n        <ul>\n            <li class="grid_4 alpha">\n                <a href="')
        # SOURCE LINE 100
        __M_writer(escape(h.url_for(controller='page', action='home')))
        __M_writer(u'" title="Home">\n                    Home <span>Some content here</span>\n                </a>\n            </li>\n            <li class="grid_4">\n                <a href="')
        # SOURCE LINE 105
        __M_writer(escape(h.url_for(controller='page', action='view', slug='about')))
        __M_writer(u'" title="About">\n                    About <span>About me and this site</span>\n                </a>\n            </li>\n            <li class="grid_4">\n                <a href="')
        # SOURCE LINE 110
        __M_writer(escape(h.url_for(controller='page', action='view', slug='teaching')))
        __M_writer(u'" title="Teaching">\n                    Teaching <span>My former life as a teacher</span>\n                </a>\n            </li>\n            <li class="grid_4 omega">\n                <a href="/lifestream" title="Lifestream">Lifestream <span>Some content here</span></a>\n            </li> \n        </ul>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 75
        __M_writer(u'\n    <div id="header">\n        <div class="container_16">\n            <div class="grid_16">\n                <div class="grid_8 alpha">\n                    <h1>Jason Leveille</h1>\n                    <p>Web Responsible, From Design Through Deployment</p>\n                </div>\n                <div class="grid_8 omega">\n                    <div id="subscribe" class="grid_4 alpha">\n                        <p>Subscribe</p>\n                    </div>\n                    <div id="search" class="grid_4 alpha">\n                        <p>Search</p>\n                    </div>\n                </div>\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_recent_comments(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 161
        __M_writer(u'\n    <h4>Recent Comments</h4>\n    <ul>\n        <li>Comment</li>\n        <li>Comment</li>\n        <li>Comment</li>\n        <li>Comment</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_twitter_updates(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 121
        __M_writer(u'\n    <h4>Twitter Updates</h4>\n    <ul>\n        <li>Update</li>\n        <li>Update</li>\n        <li>Update</li>\n        <li>Update</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_css(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 67
        __M_writer(u'\n    ')
        # SOURCE LINE 68
        __M_writer(escape(h.stylesheet_link(h.url_for('/css/reset.css'), media="screen, projection")))
        __M_writer(u'\n    ')
        # SOURCE LINE 69
        __M_writer(escape(h.stylesheet_link(h.url_for('/css/text.css'), media="screen, projection")))
        __M_writer(u'\n    ')
        # SOURCE LINE 70
        __M_writer(escape(h.stylesheet_link(h.url_for('/css/960.css'), media="screen, projection")))
        __M_writer(u'\n    ')
        # SOURCE LINE 71
        __M_writer(escape(h.stylesheet_link(h.url_for('/css/base.css'), media="screen, projection")))
        __M_writer(u'\n    ')
        # SOURCE LINE 72
        __M_writer(escape(h.stylesheet_link(h.url_for('/css/print.css'), media="print")))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_js(context):
    context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 232
        __M_writer(u'\n    <script type="text/javascript">\n        var djConfig = {\n            isDebug:false, \n            parseOnLoad:true\n        };\n    </script>\n    <script src="http://ajax.googleapis.com/ajax/libs/dojo/1.2/dojo/dojo.xd.js"></script>\n    ')
        # SOURCE LINE 240
        __M_writer(escape(h.javascript_link(h.url_for('/javascripts/application.js'))))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_categories(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 131
        __M_writer(u'\n    <h4>Categories</h4>\n    <ul>\n        <li>Category</li>\n        <li>Category</li>\n        <li>Category</li>\n        <li>Category</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_archives(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 141
        __M_writer(u'\n    <h4>Archives</h4>\n    <ul>\n        <li>Archive</li>\n        <li>Archive</li>\n        <li>Archive</li>\n        <li>Archive</li>\n    </ul>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


