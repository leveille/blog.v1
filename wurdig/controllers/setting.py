import datetime as d
import formencode
import logging
import re
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import webhelpers.paginate as paginate

from authkit.authorize.pylons_adaptors import authorize
from formencode import htmlfill
from paste.deploy.converters import asbool
from pylons import app_globals, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from pylons.i18n.translation import _
from sqlalchemy import func
from sqlalchemy.sql import and_, delete
from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class Cleanup(formencode.FancyValidator):
    def _to_python(self, value, state):
        # clean up value['value'] if type is boolean
        if value['type'] == 'b':
            v = value.get('value', None)
            if v is None:
                value['value'] = u'false'
            else:
                value['value'] = u'true'
        return value
    
class SettingForm(formencode.Schema):
    pre_validators = [Cleanup()]
    allow_extra_fields = True
    filter_extra_fields = True
    type = formencode.validators.UnicodeString(
        not_empty=True,
        max=2,
        strip=True
    )
    value = formencode.validators.UnicodeString(
        not_empty=False,
        strip=True
    )

class SettingController(BaseController):
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):

        try:
            id = int(id)
        except:
            abort(400)
            
        setting_q = meta.Session.query(model.Setting)
        c.setting = setting_q.filter_by(id=id).first()
        if c.setting is None:
            abort(404)
        values = {
            'id': c.setting.id,
            'key': c.setting.key,
            'value': c.setting.value
        }
        if c.setting.type == 'b':
            values['value'] = asbool(c.setting.value)
        return htmlfill.render(render('/derived/setting/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=SettingForm(), form='edit')
    def save(self, id=None):

        try:
            id = int(id)
        except:
            abort(400)
            
        setting_q = meta.Session.query(model.Setting)
        c.setting = setting_q.filter_by(id=id).first()
        if c.setting is None:
            abort(404)
            
        for k,v in self.form_result.items():
            if getattr(c.setting, k) != v:
                setattr(c.setting, k, v)
            
        meta.Session.commit()
        session['flash'] = _('Setting successfully updated.')
        session.save()
        
        # update settings cache object
        tmpl_cache = app_globals.cache.get_cache('base._setup')
        tmpl_cache.remove_value('settings')
                
        return redirect_to(controller='setting', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        
        settings_q = meta.Session.query(model.Setting).order_by([model.Setting.id])
        
        try:
            settings_page = int(request.params.get('settings_page', 1))
        except:
            abort(400)
            
        c.paginator = paginate.Page(
            settings_q,
            page=settings_page,
            items_per_page = 25,
            controller='setting',
            action='list',
        )
        return render('/derived/setting/list.html')
    
