import helpers as h
from pylons import config
import feedparser

__all__ = ['delicious', 'flickr', 'twitter']

def delicious():
    delicious_feed = feedparser.parse('http://feeds.delicious.com/v2/rss/%s?count=10' % config['delicious.username'])
    if len(delicious_feed.entries):
        items = []
        template = """
        <div id="delicious-bookmarks">
            <h4>Bookmarks</h4>
            <ul>
                %s
            </ul>
        </div>
        """
        for entry in delicious_feed.entries[:6]:
            i = '<li>%s</li>'
            link = '<a href="%s" title="%s">%s</a> (%s)'
            link = link % (entry['guid'], entry['title'], entry['title'], entry.updated[:14])
            items.append(i % link)
        return template % '\n'.join(items)
    else:
        return ''
    
def flickr():
    flickr_feed = feedparser.parse('http://api.flickr.com/services/feeds/photos_public.gne?id=%s@N00&lang=en-us&format=atom' % config['flickr.id'])
    if len(flickr_feed.entries):
        items = []
        template = """
        <div id="flickr-images">
            <h4>Public Flickr Stream</h4>
            <ul>
                %s
            </ul>
        </div>
        """
        for entry in flickr_feed.entries[:5]:
            image = entry['enclosures'][0]['href']
            image = image.replace('m.jpg', 's.jpg')
            i = '<li>%s</li>' % h.link_to(
                                        h.literal('<img src="%s" title="%s">' % (image, entry['title'])),
                                        entry['link']
                                        )
            items.append(i)
        return template % '\n'.join(items)
    else:
        return ''

def twitter():
    twitter_feed = feedparser.parse("http://twitter.com/statuses/user_timeline/%s.rss" % config['twitter.user.screen_name'])
    if len(twitter_feed.entries):
        items = []
        template = """
        <div id="twitter-statuses">
            <h4>Twitter Updates</h4>
            <ul>
                %s
            </ul>
        </div>
        """
        for entry in twitter_feed.entries[:5]:
            i = '<li>%s<span>%s</span></li>' % (h.auto_link(entry['description']),
                                                h.link_to(
                                                entry.updated[:14],
                                                entry['guid'])
                                                )
            items.append(i)
        return template % '\n'.join(items)
    else:
        return ''