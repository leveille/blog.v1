from authkit.permissions import ValidAuthKitUser
from authkit.permissions import HasAuthKitRole
from authkit.authorize.pylons_adaptors import authorized
from pylons.templating import render_mako as render
from authkit.authorize.pylons_adaptors import authorize

is_valid_user = ValidAuthKitUser()
has_delete_role = HasAuthKitRole(['delete'])

def render_signin():
    return render('/derived/account/signin.html').encode('utf-8')