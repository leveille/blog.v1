import helpers as h
from pylons import tmpl_context as c
from pylons.i18n.translation import _, get_lang

__all__ = ['delicious', 'flickr', 'twitter']

def delicious():
    if not c.enable_delicious_display:
        return u''
    
    delicious_feed = feedparser.parse('http://feeds.delicious.com/v2/rss/%s?count=10' % c.settings.get('delicious_username'))
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
        return u''

def flickr():
    if not c.enable_flickr_display:
        return u''
    
    html = """
    <div id="wurdig-flickr-feed">
        <h4>%s</h4>
        %s
    </div>
    """  % (_('Public Flickr Stream'), """
    <object width="100%" height="310"> 
        <param name="flashvars" 
            value="offsite=true&lang=en-us&page_show_url=%2Fphotos%2Fleveille%2Fshow%2F&page_show_back_url=%2Fphotos%2F{{username}}%2F&user_id={{flickr_id}}&jump_to="></param> 
        <param name="movie" value="http://www.flickr.com/apps/slideshow/show.swf?v=71649"></param> 
        <param name="allowFullScreen" value="true"></param>
        <embed type="application/x-shockwave-flash" 
            src="http://www.flickr.com/apps/slideshow/show.swf?v=71649" 
            allowFullScreen="true" 
            flashvars="offsite=true&lang=en-us&page_show_url=%2Fphotos%2Fleveille%2Fshow%2F&page_show_back_url=%2Fphotos%2F{{username}}%2F&user_id={{flickr_id}}&jump_to=" 
            width="100%" height="310">
        </embed>
    </object>
    """)
    html = html.replace('{{flickr_id}}', c.settings.get('flickr_id'))
    # @todo: Add a setting entry for the flickr username (though this isn't my flickr username)
    html = html.replace('{{username}}', 'leveille')
    return html

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