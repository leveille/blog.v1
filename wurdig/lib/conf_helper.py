from pylons import tmpl_context as c
from pylons.i18n.translation import _

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
           'wurdig_googleanalytics_key',
           'wurdig_use_googleanalytics',
           'wurdig_external_posts_feed',
           'wurdig_use_externalposts_feed',
           ]

def wurdig_get_akismet_key():
    return c.settings.get('akismet_key', _('Error retrieving akismet key'))

def wurdig_use_akismet():
    return c.enable_akismet

def wurdig_spamword():
    return c.settings.get('spamword', _('Error retrieving spamword'))

def wurdig_title():
    return c.settings.get('site_title', _('Error retrieving site title'))

def wurdig_subtitle():
    return c.settings.get('site_tagline', _('Error retrieving site tagline'))

def wurdig_use_subtitle():
    return c.display_tagline

def wurdig_contact_email():
    return c.settings.get('admin_email', _('Error retrieving admin email'))

def wurdig_display_contact_email():
    return c.display_admin_email

def wurdig_googlesearch_key():
    return c.settings.get('googlesearch_key', _('Error retrieving Google search key'))

def wurdig_use_googlesearch():
    return c.enable_googlesearch

def wurdig_googleanalytics_key():
    return c.settings.get('googleanalytics_key', _('Error retrieving Google analytics key'))

def wurdig_use_googleanalytics():
    return c.enable_googleanalytics

def wurdig_external_posts_feed():
    return c.settings.get('externalposts_feed_url', _('Error retrieving external posts feed url'))

def wurdig_use_externalposts_feed():
    return c.use_externalposts_feed
