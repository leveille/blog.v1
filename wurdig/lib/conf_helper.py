from pylons import config

__all__ = ['wurdig_use_akismet', 
           'wurdig_get_akismet_key',
           'wurdig_spamword', 
           'wurdig_title',
           'wurdig_subtitle',
           'wurdig_use_subtitle',
           'wurdig_comment_adminname',
           'wurdig_contact_email',
           'wurdig_display_contact_email',
           ]

def wurdig_use_akismet():
    try:
        akistmet_key = config['akismet.api_key']
    except Exception, e:
        akistmet_key = None
    return config['akismet.api_key'] not in ['', None, u'']

def wurdig_get_akismet_key():
    if wurdig_use_akismet():
        return config['akismet.api_key']
        # should I rais an exception here?
    return u'' 

def wurdig_spamword():
    try:
        wurdig_spamword = config['blog.spamword']
    except Exception, e:
        wurdig_spamword = u'wurdig'
    return wurdig_spamword

def wurdig_title():
    try:
        wurdig_title = config['blog.title']
    except Exception, e:
        wurdig_title = u'Please enter a blog title in your main configuration file: blog.title'
    return wurdig_title

def wurdig_subtitle():
    try:
        wurdig_subtitle = config['blog.subtitle']
    except Exception, e:
        wurdig_subtitle = None
    return wurdig_subtitle

def wurdig_use_subtitle():
    return wurdig_subtitle() not in ['', None, u'']

def wurdig_comment_adminname():
    try:
        wurdig_comment_adminname = config['blog.comment.admin']
    except Exception, e:
        wurdig_comment_adminname = None
    return wurdig_comment_adminname

def wurdig_contact_email():
    try:
        wurdig_contact = config['blog.contact']
    except Exception, e:
        wurdig_contact = None
    return wurdig_contact

def wurdig_display_contact_email():
    try:
        wurdig_display_contact = config['blog.display.contact']
    except Exception, e:
        wurdig_display_contact = None
    return wurdig_display_contact not in ['', None, u'']