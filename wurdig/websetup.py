"""Setup the Wurdig application"""
import logging
import os.path
import datetime

from authkit.users.sqlalchemy_driver import UsersFromDatabase
from authkit.users import md5
from wurdig import model
from wurdig.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    load_environment(conf.global_conf, conf.local_conf)

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
    
    setting1 = model.Setting()
    setting1.key = u'site_title'
    setting1.value = u'My Wurdig Blog'
    meta.Session.add(setting1)
    meta.Session.flush()
    
    setting2 = model.Setting()
    setting2.key = u'site_tagline'
    setting2.value = u'Just Another Wurdig Blog'
    meta.Session.add(setting2)
    meta.Session.flush()
    
    setting_display_tagline = model.Setting()
    setting_display_tagline.key = u'display_tagline'
    setting_display_tagline.value = u'True'
    meta.Session.add(setting_display_tagline)
    meta.Session.flush()
    
    setting3 = model.Setting()
    setting3.key = u'admin_email'
    setting3.value = u'json.leveille@gmail.com'
    meta.Session.add(setting3)
    meta.Session.flush()
    
    setting4 = model.Setting()
    setting4.key = u'display_admin_email'
    setting4.value = u'False'
    meta.Session.add(setting4)
    meta.Session.flush()
    
    setting5 = model.Setting()
    setting5.key = u'spamword'
    setting5.value = u'wurdig'
    meta.Session.add(setting5)
    meta.Session.flush()
    
    setting6 = model.Setting()
    setting6.key = u'enable_googlesearch'
    setting6.value = u'False'
    meta.Session.add(setting6)
    meta.Session.flush()
    
    setting7 = model.Setting()
    setting7.key = u'googlesearch_key'
    setting7.value = u''
    meta.Session.add(setting7)
    meta.Session.flush()
    
    setting8 = model.Setting()
    setting8.key = u'enable_googleanalytics'
    setting8.value = u'False'
    meta.Session.add(setting8)
    meta.Session.flush()
    
    setting9 = model.Setting()
    setting9.key = u'googleanalytics_key'
    setting9.value = u''
    meta.Session.add(setting9)
    meta.Session.flush()
    
    setting10 = model.Setting()
    setting10.key = u'enable_akismet'
    setting10.value = u'False'
    meta.Session.add(setting10)
    meta.Session.flush()
    
    setting11 = model.Setting()
    setting11.key = u'akismet_key'
    setting11.value = u''
    meta.Session.add(setting11)
    meta.Session.flush()
    
    setting12 = model.Setting()
    setting12.key = u'enable_twitter_display'
    setting12.value = u'False'
    meta.Session.add(setting12)
    meta.Session.flush()
    
    setting13 = model.Setting()
    setting13.key = u'twitter_screenname'
    setting13.value = u''
    meta.Session.add(setting13)
    meta.Session.flush()
    
    setting14 = model.Setting()
    setting14.key = u'enable_delicious_display'
    setting14.value = u'False'
    meta.Session.add(setting14)
    meta.Session.flush()
    
    setting15 = model.Setting()
    setting15.key = u'delicious_username'
    setting15.value = u''
    meta.Session.add(setting15)
    meta.Session.flush()
    
    setting16 = model.Setting()
    setting16.key = u'enable_flickr_display'
    setting16.value = u'False'
    meta.Session.add(setting16)
    meta.Session.flush()
    
    setting17 = model.Setting()
    setting17.key = u'flickr_id'
    setting17.value = u''
    meta.Session.add(setting17)
    meta.Session.flush()
    
    setting18 = model.Setting()
    setting18.key = u'use_minified_assets'
    setting18.value = u'False'
    meta.Session.add(setting18)
    meta.Session.flush()
    
    setting19 = model.Setting()
    setting19.key = u'use_externalposts_feed'
    setting19.value = u'False'
    meta.Session.add(setting19)
    meta.Session.flush()
    
    setting20 = model.Setting()
    setting20.key = u'externalposts_feed_url'
    setting20.value = u''
    meta.Session.add(setting20)
    meta.Session.flush()
    
    setting21 = model.Setting()
    setting21.key = u'blogroll'
    setting21.value = u"""
    <h4>Blogroll</h4>
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
    """
    meta.Session.add(setting21)
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
