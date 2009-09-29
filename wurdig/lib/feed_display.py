import feedparser
import helpers as h
from pylons import tmpl_context as c
from pylons.i18n.translation import _, get_lang

__all__ = ['delicious', 'flickr', 'twitter']

def delicious():
    if not c.enable_delicious_display:
        return u''
    
    html = """
    <div id="wurdig-delicious-feed" class="wurdig-secondary-list">
        <h4>%s</h4>
        <script type="text/javascript" src="http://feeds.delicious.com/v2/js/%s?title=&count=8&sort=date&extended"></script>
    </div>
    """ % (
        _('Bookmarks'),
        c.settings.get('delicious_username')
    )
    
    return html

def flickr():
    if not c.enable_flickr_display:
        return u''
    
    flickr_feed = feedparser.parse('http://api.flickr.com/services/feeds/photos_public.gne?id=%s&lang=%s&format=atom' % (c.settings.get('flickr_id'), get_lang()))

    if len(flickr_feed.entries):
        items = []
        template = """
        <div id="wurdig-flickr-feed">
            <h4>%s</h4>
            <ul>
                %s
            </ul>
        </div>
        """
        for entry in flickr_feed.entries[:12]:
            image = entry['enclosures'][0]['href']
            image = image.replace('m.jpg', 's.jpg')
            i = '<li>%s</li>' % h.link_to(
                                        h.literal('<img src="%s" title="%s" alt="%s">' % (image, entry['title'], entry['title'])),
                                        entry['link']
                                        )
            items.append(i)
        return template % (_('Public Flickr Stream'), '\n'.join(items))
    else:
        return u''

def twitter():
    if not c.enable_twitter_display:
        return u''
    
    html = """
        <div id="wurdig-twitter-feed" class="wurdig-sidebar-list">
        <h4>%s</h4>
        <div id="twtr-profile-widget"></div>
        <script src="http://widgets.twimg.com/j/1/widget.js"></script>
        <link href="http://widgets.twimg.com/j/1/widget.css" type="text/css" rel="stylesheet">
        <script>
        new TWTR.Widget({
          profile: true,
          id: 'twtr-profile-widget',
          loop: true,
          width: 227,
          height: 300,
          theme: {
            shell: {
              background: '#f3f3f3',
              color: '#000'
            },
            tweets: {
              background: '#ffffff',
              color: '#444444',
              links: '#1985b5'
            }
          }
        }).render().setProfile('%s').start();
        </script>
        </div>
    """ % (_('Twitter Updates'), c.settings.get('twitter_screenname'))
    
    return html