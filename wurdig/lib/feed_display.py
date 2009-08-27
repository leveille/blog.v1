import feedparser
import helpers as h
from pylons import config
from pylons.i18n.translation import _

__all__ = ['delicious', 'flickr', 'twitter']

def delicious():
    delicious_feed = feedparser.parse('http://feeds.delicious.com/v2/rss/%s?count=10' % config['delicious.username'])
    if len(delicious_feed.entries):
        items = []
        template = """
        <div id="wurdig-delicious-feed" class="wurdig-secondary-list">
            <h4>%s</h4>
            <ul>
                %s
            </ul>
        </div>
        """
        for entry in delicious_feed.entries[:7]:
            i = '<li>%s</li>'
            link = '<a href="%s" title="%s">%s (%s)</a>'
            link = link % (entry['guid'], entry['title'], entry['title'], entry.updated[:11])
            items.append(i % link)
        return template % (_('Bookmarks'), '\n'.join(items))
    else:
        return ''

def flickr():
    flickr_feed = feedparser.parse('http://api.flickr.com/services/feeds/photos_public.gne?id=%s@N00&lang=en-us&format=atom' % config['flickr.id'])
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
        return ''

def twitter():
    twitter_feed = feedparser.parse("http://twitter.com/statuses/user_timeline/%s.rss" % config['twitter.user.screen_name'])
    if len(twitter_feed.entries):
        items = []
        template = """
        <div id="wurdig-twitter-feed" class="wurdig-sidebar-list">
            <h4>%s (<a href="http://twitter.com/%s">%s</a>)</h4>
            <ul>
                %s
            </ul>
        </div>
        """

        for entry in twitter_feed.entries[:4]:
            description = entry['description'].split(':', 1)[1]
            i = '<li><span class="lone">%s</span> <span>%s</span></li>' % (h.link_to(
                                                entry.updated,
                                                entry['guid']),
                                                h.auto_link(description)
                                                )
            items.append(i)
        return template % (_('Twitter Updates'), 
                           config['twitter.user.screen_name'], 
                           _('Follow'),
                           '\n'.join(items))
    else:
        return ''