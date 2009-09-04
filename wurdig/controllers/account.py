import formencode
import logging
import webhelpers.paginate as paginate
import wurdig.lib.helpers as h
import wurdig.model as model
import wurdig.model.meta as meta

from formencode import htmlfill
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.i18n.translation import _
from sqlalchemy.sql import and_
from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ValidLogin(formencode.FancyValidator):
    messages = {
        'invalid': _('You entered an invalid username or password')
    }
    def _to_python(self, values, state):
        user_q = meta.Session.query(model.User).filter(
            and_(
                model.User.username == values['username'], 
                model.User.password == values['password']
            )
        )
        if user_q is None:
            raise formencode.Invalid(
                self.message('invalid', state),
                values, state
            )
        return values

class MyLoginForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    username = formencode.validators.UnicodeString(
        not_empty=True,
        max=15, 
        messages={
            'empty': _('Enter a username')
        },
        strip=True
    )
    password = formencode.validators.UnicodeString(
        not_empty=True,
        max=25, 
        messages={
            'empty': _('Enter a password')
        },
        strip=True
    )
    chained_validators = [ValidLogin()]

class AccountController(BaseController):

    # @validate(schema=MyLoginForm(), form='signin')
    # need to figure out why validation is failing
    def dashboard(self):
        if not request.environ.get('REMOTE_USER'):
            # This triggers the AuthKit middleware into displaying the sign-in form
            abort(401)
        else:
            self._recent_comments()
            self._drafts()
            self._settings()
            return render('/derived/account/dashboard.html')

    def signout(self):
        # The actual removal of the AuthKit cookie occurs when the response passes
        # through the AuthKit middleware, we simply need to display a page
        # confirming the user is signed out
        return render('/derived/account/signedout.html')

    def signinagain(self):
        request.environ['paste.auth_tkt.logout_user']()
        return render('/derived/account/signin.html').replace('%s', h.url_for('dashboard'))
    
    def _recent_comments(self):
        # Get recent comments
        comments_q = meta.Session.query(model.Comment).order_by(
                                               model.Comment.approved
                                               ).order_by(model.Comment.created_on.desc())
        comments_q = comments_q.all()
        
        try:
            comment_page = int(request.params.get('comment_page', 1))
        except:
            abort(400)
        
        c.comment_paginator = paginate.Page(
            comments_q,
            page=comment_page,
            items_per_page=5,
            controller='account',
            action='dashboard'
        )
        
    def _drafts(self):
        posts_q = meta.Session.query(model.Post).filter(model.Post.draft == True).order_by([model.Post.created_on.desc()])
        
        try:
            posts_page = int(request.params.get('posts_page', 1))
        except:
            abort(400)
        
        c.draft_paginator = paginate.Page(
            posts_q,
            page=posts_page,
            items_per_page = 5,
            controller='account',
            action='dashboard',
        )
        
    def _settings(self):
        settings_q = meta.Session.query(model.Setting).order_by([model.Setting.id])
        
        try:
            settings_page = int(request.params.get('settings_page', 1))
        except:
            abort(400)
            
        c.settings_paginator = paginate.Page(
            settings_q,
            page=settings_page,
            items_per_page = 15,
            controller='account',
            action='dashboard',
        )