import formencode
import logging
import wurdig.lib.helpers as h
import wurdig.model as model
import wurdig.model.meta as meta

from formencode import htmlfill
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from sqlalchemy.sql import and_
from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ValidLogin(formencode.FancyValidator):
    messages = {
        'invalid': 'You entered an invalid username or password'
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
            'empty':'Enter a username'
        },
        strip=True
    )
    password = formencode.validators.UnicodeString(
        not_empty=True,
        max=25, 
        messages={
            'empty':'Enter a password'
        },
        strip=True
    )
    chained_validators = [ValidLogin()]

class AccountController(BaseController):

    # @validate(schema=MyLoginForm(), form='signin')
    # need to figure out why validation is failing
    def signin(self):
        if not request.environ.get('REMOTE_USER'):
            # This triggers the AuthKit middleware into displaying the sign-in form
            abort(401)
        else:
            return render('/derived/account/signedin.html')

    def signout(self):
        # The actual removal of the AuthKit cookie occurs when the response passes
        # through the AuthKit middleware, we simply need to display a page
        # confirming the user is signed out
        return render('/derived/account/signedout.html')

    def signinagain(self):
        request.environ['paste.auth_tkt.logout_user']()
        return render('/derived/account/signin.html').replace('%s', h.url_for('signin'))
    