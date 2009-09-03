"""Setup the Wurdig application"""
import logging
import os.path
import datetime

from authkit.users.sqlalchemy_driver import UsersFromDatabase
from authkit.users import md5
from pylons.i18n.translation import _
from wurdig import model
from wurdig.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    load_environment(conf.global_conf, conf.local_conf)
    
    # http://pylonshq.com/project/pylonshq/ticket/509
    from pylons.i18n.translation import _get_translator
    import pylons
    pylons.translator._push_object(_get_translator(pylons.config.get('lang')))

    from wurdig.model import meta
    meta.metadata.bind = meta.engine
    
    users = UsersFromDatabase(model)
    
    filename = os.path.split(conf.filename)[-1]
    if filename == 'test.ini':
        # Permanently drop any existing tables
        meta.metadata.drop_all(checkfirst=True)
        
    # Create the tables if they aren't there already
    meta.metadata.create_all(checkfirst=True)
    
    users.role_create("admin")
    users.user_create("admin", password=md5("admin"))
    users.user_add_role("admin", role="admin")
    
    setting_site_title = model.Setting()
    setting_site_title.key = u'site_title'
    setting_site_title.value = u'My Wurdig Blog'
    setting_site_title.description = _(u'Site Title?')
    setting_site_title.help = _(u'What is the title of this '
                                'site (ex. Jason Leveille\'s Blog)?')
    meta.Session.add(setting_site_title)
    meta.Session.flush()
    
    setting_site_tagline = model.Setting()
    setting_site_tagline.key = u'site_tagline'
    setting_site_tagline.value = u'Just Another Wurdig Blog'
    setting_site_tagline.description = _(u'Site Tagline?')
    setting_site_tagline.help = _(u'What is the tagline of this site?')
    meta.Session.add(setting_site_tagline)
    meta.Session.flush()
    
    setting_display_tagline = model.Setting()
    setting_display_tagline.key = u'display_tagline'
    setting_display_tagline.value = u'true'
    setting_display_tagline.description = _(u'Display Site Tagline?')
    setting_display_tagline.type = u'b'
    setting_display_tagline.help = _(u'Should the tagline be shown for your site?')
    meta.Session.add(setting_display_tagline)
    meta.Session.flush()
    
    setting_admin_email = model.Setting()
    setting_admin_email.key = u'admin_email'
    setting_admin_email.value = u''
    setting_admin_email.description = _(u'Administrator Email')
    setting_admin_email.help = _(u'What is the administrator email for this site?  '
                                 'This will be used for notifications, to send email, etc?')
    meta.Session.add(setting_admin_email)
    meta.Session.flush()
    
    setting_display_admin_email = model.Setting()
    setting_display_admin_email.key = u'display_admin_email'
    setting_display_admin_email.value = u'false'
    setting_display_admin_email.description = _(u'Display Admin Email?')
    setting_display_admin_email.type = u'b'
    setting_display_admin_email.help = _(u'Should the administrator email be '
                                         'display (obfuscated) publicly?')
    meta.Session.add(setting_display_admin_email)
    meta.Session.flush()
    
    setting_spamword = model.Setting()
    setting_spamword.key = u'spamword'
    setting_spamword.value = u'wurdig'
    setting_spamword.description = _(u'Your Spam Deterrent Word?')
    setting_spamword.help = _(u'If you enable Akismet this spamword '
                              'becomes irrelevant.  Otherwise, what is '
                              'your spam deterrent word (used in comments)?')
    meta.Session.add(setting_spamword)
    meta.Session.flush()
    
    setting_enable_googlesearch = model.Setting()
    setting_enable_googlesearch.key = u'enable_googlesearch'
    setting_enable_googlesearch.value = u'false'
    setting_enable_googlesearch.description = _(u'Enable Google Search?')
    setting_enable_googlesearch.type = u'b'
    setting_enable_googlesearch.help = _(u'Should Google Search be enabled?  '
                                         'If so, you\'ll need a Google Search '
                                         'Key (http://www.google.com/sitesearch/).')
    meta.Session.add(setting_enable_googlesearch)
    meta.Session.flush()
    
    setting_googlesearch_key = model.Setting()
    setting_googlesearch_key.key = u'googlesearch_key'
    setting_googlesearch_key.value = u''
    setting_googlesearch_key.description = _(u'Your Google Search Key?')
    setting_googlesearch_key.help = _(u'What is your Google Search Key '
                                      '(http://www.google.com/sitesearch/)?  '
                                      'Only relevant if you have Google search enabled.')
    meta.Session.add(setting_googlesearch_key)
    meta.Session.flush()
    
    setting_enable_googleanalytics = model.Setting()
    setting_enable_googleanalytics.key = u'enable_googleanalytics'
    setting_enable_googleanalytics.value = u'false'
    setting_enable_googleanalytics.description = _(u'Enable Google Analytics?')
    setting_enable_googleanalytics.type = u'b'
    setting_enable_googleanalytics.help = _(u'Do you want to enable Google Analytics?')
    meta.Session.add(setting_enable_googleanalytics)
    meta.Session.flush()
    
    setting_googleanalytics_key = model.Setting()
    setting_googleanalytics_key.key = u'googleanalytics_key'
    setting_googleanalytics_key.value = u''
    setting_googleanalytics_key.description = _(u'Your Google Analytics Key?')
    setting_googleanalytics_key.help = _(u'What is your Google Analytics key?')
    meta.Session.add(setting_googleanalytics_key)
    meta.Session.flush()
    
    setting_enable_akismet = model.Setting()
    setting_enable_akismet.key = u'enable_akismet'
    setting_enable_akismet.value = u'false'
    setting_enable_akismet.description = _(u'Enable Akismet Spam Detection?')
    setting_enable_akismet.type = u'b'
    setting_enable_akismet.help = _(u'Do you want to enable Akismet spam '
                                    'detection?  You\'ll need an Akismet '
                                    'API key (http://akismet.com/personal/).')
    meta.Session.add(setting_enable_akismet)
    meta.Session.flush()
    
    setting_akismet_key = model.Setting()
    setting_akismet_key.key = u'akismet_key'
    setting_akismet_key.value = u''
    setting_akismet_key.description = _(u'Your Akismet API Key?')
    setting_akismet_key.help = _(u'What is your Akismet API Key '
                                 '(http://akismet.com/personal/)?')
    meta.Session.add(setting_akismet_key)
    meta.Session.flush()
    
    setting_enable_twitter_display = model.Setting()
    setting_enable_twitter_display.key = u'enable_twitter_display'
    setting_enable_twitter_display.value = u'false'
    setting_enable_twitter_display.description = _(u'Enable Twitter Display?')
    setting_enable_twitter_display.type = u'b'
    setting_enable_twitter_display.help = _(u'Do you want to display '
                                            'your latest tweets?')
    meta.Session.add(setting_enable_twitter_display)
    meta.Session.flush()
    
    setting_twitter_screenname = model.Setting()
    setting_twitter_screenname.key = u'twitter_screenname'
    setting_twitter_screenname.value = u''
    setting_twitter_screenname.description = u'Your Twitter Screen Name?'
    setting_twitter_screenname.help = _(u'What is your Twitter screen name?')
    meta.Session.add(setting_twitter_screenname)
    meta.Session.flush()
    
    setting_enable_delicious_display = model.Setting()
    setting_enable_delicious_display.key = u'enable_delicious_display'
    setting_enable_delicious_display.value = u'false'
    setting_enable_delicious_display.description = _(u'Enable Delicious Bookmarks Display?')
    setting_enable_delicious_display.type = u'b'
    setting_enable_delicious_display.help = _(u'Do you want to display your '
                                              'Delicious bookmarks '
                                              '(http://delicious.com/)?')
    meta.Session.add(setting_enable_delicious_display)
    meta.Session.flush()
    
    setting_delicious_username = model.Setting()
    setting_delicious_username.key = u'delicious_username'
    setting_delicious_username.value = u''
    setting_delicious_username.description = _(u'Your Delicious User Name?')
    setting_delicious_username.help = _(u'What is your Delicious user name?')
    meta.Session.add(setting_delicious_username)
    meta.Session.flush()
    
    setting_enable_flickr_display = model.Setting()
    setting_enable_flickr_display.key = u'enable_flickr_display'
    setting_enable_flickr_display.value = u'false'
    setting_enable_flickr_display.description = _(u'Enable Flickr Image Display?')
    setting_enable_flickr_display.type = u'b'
    setting_enable_flickr_display.help = _(u'Do you want to display '
                                           'images from your Flickr account?')
    meta.Session.add(setting_enable_flickr_display)
    meta.Session.flush()
    
    setting_flickr_id = model.Setting()
    setting_flickr_id.key = u'flickr_id'
    setting_flickr_id.value = u''
    setting_flickr_id.description = _(u'Your Flickr ID?')
    setting_flickr_id.help = _(u'What is your Flickr ID (http://idgettr.com/)?')
    meta.Session.add(setting_flickr_id)
    meta.Session.flush()
    
    setting_use_minified_assets = model.Setting()
    setting_use_minified_assets.key = u'use_minified_assets'
    setting_use_minified_assets.value = u'false'
    setting_use_minified_assets.description = _(u'Use Minified Assets (CSS/JS)?')
    setting_use_minified_assets.type = u'b'
    setting_use_minified_assets.help = _(u'Do you want to combine and '
                                         'minify your js/css files?  If '
                                         'you\'re unsure, don\'t do anything.')
    meta.Session.add(setting_use_minified_assets)
    meta.Session.flush()
    
    setting_use_externalposts_feed = model.Setting()
    setting_use_externalposts_feed.key = u'use_externalposts_feed'
    setting_use_externalposts_feed.value = u'false'
    setting_use_externalposts_feed.description = _(u'Use External Posts Feed (ex. Feedburner)?')
    setting_use_externalposts_feed.type = u'b'
    setting_use_externalposts_feed.help = _(u'Do you want to point your '
                                            'blog posts feed at an external URL?')
    meta.Session.add(setting_use_externalposts_feed)
    meta.Session.flush()
    
    setting_externalposts_feed_url = model.Setting()
    setting_externalposts_feed_url.key = u'externalposts_feed_url'
    setting_externalposts_feed_url.value = u''
    setting_externalposts_feed_url.description = _(u'Your External Posts Feed URL?')
    setting_externalposts_feed_url.help = _(u'What is the external URL '
                                            'that contains your post feed '
                                            '(ex. http://feeds2.feedburner.com/leveille)?')
    meta.Session.add(setting_externalposts_feed_url)
    meta.Session.flush()
    
    setting_blogroll = model.Setting()
    setting_blogroll.key = u'blogroll'
    setting_blogroll.value = u"""
    <h4>%s</h4>
    <ul>
        <li><a title="456 Berea Street" rel="external" href="http://www.456bereastreet.com/">456 Berea Street</a></li>
        <li><a title="Ben Ramsey" rel="external" href="http://benramsey.com/">Ben Ramsey</a></li>
        <li><a title="Daytime Running Lights" rel="external" href="http://jchrisa.net">Daytime Running Lights</a></li>
        <li><a title="Eric Florenzano" rel="external" href="http://www.eflorenzano.com">Eric Florenzano</a></li>
        <li><a title="Ian Bicking" rel="external" href="http://blog.ianbicking.org/">Ian Bicking</a></li>
        <li><a title="Chris Shiflett" rel="external" href="http://shiflett.org/">Chris Shiflett</a></li>
        <li><a title="Simon Willison" rel="external" href="http://simonwillison.net/">Simon Willison</a></li>
        <li><a title="Teach Me the Web" rel="external" href="http://teachmetheweb.org/">Teach Me the Web</a></li>
        <li><a title="Travis Swicegood" rel="external" href="http://www.travisswicegood.com/index.php">Travis Swicegood</a></li>
        <li><a title="Zac Gordon" rel="external" href="http://zgordon.org/">Zac Gordon</a></li>
    </ul>
    """ % _('Blogroll')
    setting_blogroll.description = _(u'Blogroll')
    setting_blogroll.type = u'ta'
    setting_blogroll.help = _(u'Your favorite links!')
    meta.Session.add(setting_blogroll)
    meta.Session.flush()

    page1 = model.Page()
    page1.title = u'About me and this site'
    page1.slug = u'about'
    page1.content = u"""
    <p>Welcome.  My name is Jason Leveille.  I currently live (with my beautiful wife and two daughters) and attend <a href="http://www.hood.edu">graduate school (<abbr title="Master of Science in Computer Science">MSCS</abbr>)</a> in Frederick, Maryland.  June 16th, 2007 I ended my <del>6</del> <ins>8</ins> year career as a <a href="http://www.qohs.org">High School</a> <abbr title="Computer Science">CS</abbr> teacher, and June 18th, 2007 I started my new career as a web software developer with <a href="http://www.blueatlas.com">Blue Atlas Interactive</a> in Germantown, Maryland.  I had been developing web applications since 2002, and finally decided that it was something I needed to be doing full time.  While developing I mostly work with PHP and JavaScript, though I have been paid to develop web applications in .net (C#), Python (Plone), classic asp, and I have dabbled in Ruby/Rails, Django, and Pylons.  I also work closely with designers to take their PSD goodies and turn them into CSS works of art.  I have also been known to focus on issues in <a href="http://www.webstandards.org/action/edutf/examples/">web standards</a> and <a href="http://www.adainfo.org/accessible/it/events.asp">accessibility</a>.</p>
    <p>If you have any questions for me about any of my posts, feel free to leave a comment.  If that is not sufficient, my email address is leveillej [at] gmail [dot] com.</p>
    <h3>ElseWhere</h3>
    <ul>
        <li><a href="http://twitter.com/jleveille">Twitter</a></li>
        <li><a href="http://del.icio.us/leveille">Del.icio.us</a></li>
    </ul>
    <h3>Disclaimer</h3>
    <p>Views and opinions expressed on this site are mine and do not necessarily reflect the views of my fantastic employer, <a href="http://www.blueatlas.com">Blue Atlas Interactive</a>.</p>
    <h3>My Office</h3>
    <div class="wurdig-caption aligncenter" style="width: 440px;"><a href="http://www.flickr.com/photos/leveilles/3273777769/"><img title="My Office" src="http://farm4.static.flickr.com/3368/3273777769_be393f175a_b.jpg" alt="Office Image 1" width="430" height="287"></a><p class="wurdig-caption-text">Office Image 1</p></div>
    <div class="wurdig-caption aligncenter" style="width: 440px;"><a href="http://www.flickr.com/photos/leveilles/3274596830/in/photostream/"><img title="Office Image 2" src="http://farm4.static.flickr.com/3300/3274596830_ac344872d7_b.jpg" alt="Office Image 2" width="430" height="287"></a><p class="wurdig-caption-text">Office Image 2</p></div>
    """
    meta.Session.add(page1)
    meta.Session.flush()
    
    page2 = model.Page()
    page2.title = u'My life as a teacher'
    page2.slug = u'teaching'
    page2.content = u'<p>I am often asked about my old teaching material (which used to be housed at http://www.my-classes.org - <a href="http://web.archive.org/web/20071216031655/http://www.my-classes.org/">wayback</a>).  <a href="http://jasonleveille.com/teacher/">My old lessons</a> are still available (I can\'t say how relevant they still are though!).  Let me know if you have any questions.</p>'
    meta.Session.add(page2)
    meta.Session.flush()
        
    search = model.Page()
    search.title = u'Search'
    search.slug = u'search'
    search.content = u"""
    <div id="cse-search-results"></div>
        <script type="text/javascript">
            var googleSearchIframeName = "cse-search-results";
            var googleSearchFormName = "cse-search-box";
            var googleSearchFrameWidth = 600;
            var googleSearchDomain = "www.google.com";
            var googleSearchPath = "/cse";
        </script>
        <script type="text/javascript" src="http://www.google.com/afsonline/show_afs_search.js">
    </script>
    """
    meta.Session.add(search)
    meta.Session.flush()
    
    post1 = model.Post()
    post1.title = u'First test post'
    post1.slug = u'first-test-post'
    post1.content = u'<p>This is the first test post</p>'
    post1.created_on = datetime.datetime(2008, 3, 17, 12, 30, 45)
    meta.Session.add(post1)
    meta.Session.flush()
    
    post5 = model.Post()
    post5.title = u'Fifth test post'
    post5.slug = u'fifth-test-post'
    post5.content = u'<p>This is the fifth test post</p>'
    post5.created_on = datetime.datetime(2008, 3, 17, 12, 30, 45)
    post5.draft = False
    post5.posted_on = datetime.datetime(2008, 3, 18, 12, 30, 45)
    meta.Session.add(post5)
    meta.Session.flush()
    
    post2 = model.Post()
    post2.title = u'Second test post'
    post2.slug = u'second-test-post'
    post2.content = u'<p>This is the second test post</p>'
    post2.created_on = datetime.datetime(2009, 3, 24, 12, 30, 45)
    post2.draft = False
    post2.posted_on = datetime.datetime(2009, 3, 24, 12, 30, 45)
    meta.Session.add(post2)
    meta.Session.flush()
    
    post3 = model.Post()
    post3.title = u'Third test post'
    post3.slug = u'third-test-post'
    post3.content = u'<p>This is the third test post</p>'
    post3.created_on = datetime.datetime(2009, 3, 25, 12, 30, 45)
    post3.draft = False
    post3.posted_on = datetime.datetime(2009, 3, 25, 12, 30, 45)
    meta.Session.add(post3)
    meta.Session.flush()

    post4 = model.Post()
    post4.title = u'Fourth test post'
    post4.slug = u'fourth-test-post'
    post4.content = u'<p>This is the fourth test post</p>'
    post4.created_on = datetime.datetime(2009, 4, 5, 12, 30, 45)
    post4.draft = False
    post4.posted_on = datetime.datetime(2009, 4, 5, 12, 30, 45)
    meta.Session.add(post4)
    meta.Session.flush()
    
    comment1 = model.Comment()
    comment1.post_id = int(2)
    comment1.content = u'This is my comment content'
    comment1.name = u'Responsible Web'
    comment1.email = u'nomail@gmail.com'
    comment1.url = u'http://responsibleweb.com'
    meta.Session.add(comment1)
    meta.Session.flush()

    comment2 = model.Comment()
    comment2.post_id = int(2)
    comment2.content = u'This is my second comment content'
    comment2.name = u'Responsible Web'
    comment2.email = u'nomail@gmail.com'
    comment2.url = u'http://responsibleweb.com'
    comment2.approved = True
    meta.Session.add(comment2)
    meta.Session.flush()

    tag1 = model.Tag()
    tag1.name = u'Pylons'
    tag1.slug = u'pylons'
    meta.Session.add(tag1)
    meta.Session.flush()

    tag2 = model.Tag()
    tag2.name = u'Python'
    tag2.slug = u'python'
    meta.Session.add(tag2)
    meta.Session.flush()

    post_x = meta.Session.query(model.Post)
    post_y = post_x.get(int(2))
    post_z = post_x.get(int(3))
    tag_x = meta.Session.query(model.Tag)
    tag_y = tag_x.filter_by(name=u'Python').first()
    tag_z = tag_x.filter_by(name=u'Pylons').first()
    post_y.tags.append(tag_y)
    post_y.tags.append(tag_z)
    post_z.tags.append(tag_z)
    meta.Session.add(post_y)
    meta.Session.add(post_z)
    meta.Session.flush()
    
    meta.Session.commit()
    log.info('Successfully set up.')
