import base64
import pickle
from pylons import request, response

REMEMBERME_COOKIE = 'wurdig.rememberme'

__all__ = ['get_cookie', 
           'delete_cookie', 
           'get_unpickled_cookie', 
           'get_rememberme_cookie', 
           'set_rememberme_cookie', 
           'delete_rememberme_cookie']

def get_cookie(cookie):
    cookie_value = None
    try:
        cookie_value = request.cookies[cookie]
    finally:
        return cookie_value
    
def delete_cookie(cookie):
    response.delete_cookie(cookie, path='/', domain=None)
    
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

def set_rememberme_cookie(values):
    cookievalue = base64.b64encode(pickle.dumps(values))
    response.set_cookie(REMEMBERME_COOKIE, cookievalue, max_age=180*24*3600)

def delete_rememberme_cookie():
    delete_cookie(REMEMBERME_COOKIE)