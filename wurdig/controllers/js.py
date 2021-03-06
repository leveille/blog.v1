import logging
import hashlib

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, etag_cache
from pylons.decorators import jsonify
from pylons.i18n.translation import _
from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class JsController(BaseController):

    @jsonify
    def _json(self):
        translations = {
            'Are you positive you want to do that?': _('Are you positive '
                                                       'you want to do that?'),
            'The item has successfully been deleted.': _('The item has '
                                                         'successfully been deleted.'),
            'Disapprove': _('Disapprove'),
            'The item has successfully been approved.': _('The item has '
                                                          'successfully been approved.'),
            'Approve': _('Approve'),
            'The item has successfully been disapproved.': _('The item has successfully '
                                                             'been disapproved.'),
            'Your+request+has+been+completed+successfully': _('Your+request+has+been+'
                                                              'completed+successfully'),
            'An unexpected error has occurred.': _('An unexpected error has occurred.'),
            'Enter key word(s)': _('Enter key word(s)')
        }    
        return translations
        
    def translations(self):
        json_string = "if(!this.WURDIG) {var WURDIG = {};}WURDIG.translate = %s" % self._json()
        etag_cache(key=hashlib.md5(json_string).hexdigest())
        response.content_type = 'application/x-javascript; charset=utf-8'
        response.cache_control = 'max-age=2592000'
        response.pragma = ''
        return json_string