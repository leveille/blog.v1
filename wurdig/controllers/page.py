import logging
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PageController(BaseController):

    def home(self):
        return render('/derived/page/home.html')

    def view(self, slug=None):
        if slug is None:
            abort(404)
        page_q = meta.Session.query(model.Page)
        c.page = page_q.filter_by(slug=slug).first()
        if c.page is None:
            abort(404)
        c.page.content = h.literal(c.page.content)
        return render('/derived/page/view.html')