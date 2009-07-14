import base64
import pickle
from pylons import request, response

REMEMBERME_COOKIE = 'wurdig.rememberme'

__all__ = ['get_cookie', 'get_unpickled_cookie', 'get_rememberme_cookie', 'set_rememberme_cookie']

def get_cookie(cookie):
    cookie_value = None
    try:
        cookie_value = request.cookies[cookie]
    finally:
        return cookie_value

def get_unpickled_cookie(value):
    if value is None:
        return None
    
    data = None
    try:
        data = pickle.loads(base64.b64decode(value))
    finally:
        return data

def get_rememberme_cookie():
    return get_unpickled_cookie(get_cookie(REMEMBERME_COOKIE))

def set_rememberme_cookie(rememberme, comment):
    request.cookies.pop('wurdig.rememberme', None)
    if rememberme:
        values = {
            'name': comment.name,
            'email': comment.email,
            'url': comment.url, 
            'rememberme': True
        }
        cookievalue = base64.b64encode(pickle.dumps(values))
        response.set_cookie(REMEMBERME_COOKIE, cookievalue, max_age=180*24*3600)