from pylons import config

__all__ = ['wurdig_use_akismet', 
           'wurdig_get_akismet_key',
           'wurdig_spamword', 
           'wurdig_title',
           'wurdig_subtitle',
           'wurdig_use_subtitle',
           'wurdig_contact_email',
           'wurdig_display_contact_email',
           'wurdig_googlesearch_key',
           'wurdig_use_googlesearch',
           ]

def wurdig_get_akismet_key():
    try:
        akistmet_key = config['akismet.api_key']
    except Exception, e:
        akistmet_key = None
    return akistmet_key

def wurdig_use_akismet():
    return wurdig_get_akismet_key() not in ['', None, u'']

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

def wurdig_contact_email():
    try:
        wurdig_contact = config['blog.contact']
    except Exception, e:
        wurdig_contact = None
    return wurdig_contact

def wurdig_display_contact_email():
    return wurdig_contact_email() not in ['', None, u'']

def wurdig_googlesearch_key():
    try:
        wurdig_googlesearch_key = config['wurdig.googlesearch.key']
    except Exception, e:
        wurdig_googlesearch_key = None
    return wurdig_googlesearch_key

def wurdig_use_googlesearch():
    return wurdig_googlesearch_key() not in ['', None, u'']