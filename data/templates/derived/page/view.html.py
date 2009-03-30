from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 5
_modified_time = 1238419605.652868
_template_filename='/home/leveille/development/python/pylons/Wurdig/wurdig/templates/derived/page/view.html'
_template_uri='/derived/page/view.html'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['heading', 'title']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, '/base/secondary.html', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(u'\n\n<h2>')
        # SOURCE LINE 7
        __M_writer(escape(c.page.title))
        __M_writer(u'</h2>\n\n\n')
        # SOURCE LINE 10
        __M_writer(escape(c.page.content))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_heading(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 5
        __M_writer(u'<h1>')
        __M_writer(escape(c.page.title))
        __M_writer(u'</h1>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(escape(parent.title()))
        __M_writer(u' &gt; ')
        __M_writer(escape(c.page.title))
        return ''
    finally:
        context.caller_stack._pop_frame()


