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
from pylons import app_globals, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from pylons.i18n.translation import _
from sqlalchemy import func
from sqlalchemy.sql import and_, delete
from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)
    
class SettingForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    value = formencode.validators.UnicodeString(
        not_empty=False,
        messages={
            'empty': _('Enter a setting value.')
        },
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
        
        settings_q = meta.Session.query(model.Setting)
        
        try:
            page = int(request.params.get('page', 1))
        except:
            abort(400)
            
        c.paginator = paginate.Page(
            settings_q,
            page=page,
            items_per_page = 25,
            controller='setting',
            action='list',
        )
        return render('/derived/setting/list.html')
    
