import cgi

from paste.urlparser import PkgResourcesParser
from pylons import request
from pylons import tmpl_context as c
from pylons.controllers.util import forward
from pylons.middleware import error_document_template
from pylons.i18n.translation import _
from webhelpers.html.builder import literal
from wurdig.lib.base import BaseController, render

class ErrorController(BaseController):

    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """

    def document(self):
        """Render the error document"""
        resp = request.environ.get('pylons.original_response')
        code = cgi.escape(request.GET.get('code', ''))
        content = cgi.escape(request.GET.get('message', ''))
        if resp:
            content = literal(resp.status)
            code = code or cgi.escape(str(resp.status_int))
        if not code:
            raise Exception(_('No status code was found'))
        c.code = code
        c.message = content
        return render('/derived/error/document.html')

    def img(self, id):
        """Serve Pylons' stock images"""
        return self._serve_file('/'.join(['media/img', id]))

    def style(self, id):
        """Serve Pylons' stock stylesheets"""
        return self._serve_file('/'.join(['media/style', id]))

    def _serve_file(self, path):
        """Call Paste's FileApp (a WSGI application) to serve the file
        at the specified path
        """
        request.environ['PATH_INFO'] = '/%s' % path
        return forward(PkgResourcesParser('pylons', 'pylons'))
