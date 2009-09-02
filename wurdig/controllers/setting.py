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

class UniqueName(formencode.FancyValidator):
    messages = {
        'invalid': _('Setting key must be unique.')
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = formencode.validators.UnicodeString(max=30).to_python(value, state)
        # validate that tag only contains letters and undescores
        result = re.compile("[^a-zA-Z_]").search(value)
        if result:
            raise formencode.Invalid(_("Setting key can only contain "
                                       "letters and underscores."), value, state)
        
        # Ensure setting name is unique
        setting_q = meta.Session.query(model.Setting).filter_by(key=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing setting
            setting_q = setting_q.filter(model.Setting.id != int(request.urlvars['id']))
            
        # Check if the setting name exists
        key = setting_q.first()
        if key is not None:
            raise formencode.Invalid(
                self.message('invalid', state),
                value, state)
        
        return value
    
class NewSettingForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    key = UniqueName(
        not_empty=True, 
        messages={
            'empty': _('Enter a setting key.')
        },
        max=30, 
        strip=True
    )
    value = formencode.validators.UnicodeString(
        not_empty=False,
        messages={
            'empty': _('Enter a setting value.')
        },
        strip=True
    )

class SettingController(BaseController):
    
    @h.auth.authorize(h.auth.is_valid_user)
    def new(self):
        return render('/derived/setting/new.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewSettingForm(), form='new')
    def create(self):
        setting = model.Setting()
        
        for k, v in self.form_result.items():
            setattr(setting, k, v)

        meta.Session.add(setting)
        meta.Session.commit()
        session['flash'] = _('Setting successfully added.')
        session.save()
        return redirect_to(controller='setting', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):

        try:
            id = int(id)
        except:
            abort(400)
            
        setting_q = meta.Session.query(model.Setting)
        setting = setting_q.filter_by(id=id).first()
        if setting is None:
            abort(404)
        values = {
            'id': setting.id,
            'key': setting.key,
            'value': setting.value
        }
        return htmlfill.render(render('/derived/setting/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewSettingForm(), form='edit')
    def save(self, id=None):

        try:
            id = int(id)
        except:
            abort(400)
            
        setting_q = meta.Session.query(model.Setting)
        setting = setting_q.filter_by(id=id).first()
        if setting is None:
            abort(404)
            
        for k,v in self.form_result.items():
            if getattr(setting, k) != v:
                setattr(setting, k, v)
            
        meta.Session.commit()
        session['flash'] = _('Setting successfully updated.')
        session.save()
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
            items_per_page = 20,
            controller='setting',
            action='list',
        )
        return render('/derived/setting/list.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def delete_confirm(self, id=None):

        try:
            id = int(id)
        except:
            abort(400)
            
        setting_q = meta.Session.query(model.Setting)
        c.setting = setting_q.filter_by(id=id).first()
        if c.setting is None:
            abort(404)
        return render('/derived/setting/delete_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):

        try:
            id = int(request.params.getone('id'))
        except:
            abort(400)
            
        setting_q = meta.Session.query(model.Setting)
        setting = setting_q.filter_by(id=id).first()
        if setting is None:
            abort(404)
        meta.Session.delete(setting)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'%s'}" % _('The setting has been deleted')
        else:
            session['flash'] = _('Setting successfully deleted.')
            session.save()
            return redirect_to(controller='setting', action='list')
