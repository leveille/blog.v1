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
    """Place any commands to setup wurdig here"""
    load_environment(conf.global_conf, conf.local_conf)

    from wurdig.model import meta
    meta.metadata.bind = meta.engine
    
    log.info(_("Adding the AuthKit model..."))
    users = UsersFromDatabase(model)
    
    filename = os.path.split(conf.filename)[-1]
    if filename == 'test.ini':
        # Permanently drop any existing tables
        log.info(_("Dropping existing tables..."))
        meta.metadata.drop_all(checkfirst=True)
        
    # Create the tables if they aren't there already
    meta.metadata.create_all(checkfirst=True)
    
    log.info(_("Adding roles and uses..."))
    users.role_create("admin")
    users.user_create("admin", password=md5("admin"))
    users.user_add_role("admin", role="admin")
    
    log.info(_("Adding about page..."))
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
    
    log.info(_("Adding teach page..."))
    page2 = model.Page()
    page2.title = u'My life as a teacher'
    page2.slug = u'teaching'
    page2.content = u'<p>I am often asked about my old teaching material (which used to be housed at http://www.my-classes.org - <a href="http://web.archive.org/web/20071216031655/http://www.my-classes.org/">wayback</a>).  <a href="http://jasonleveille.com/teacher/">My old lessons</a> are still available (I can\'t say how relevant they still are though!).  Let me know if you have any questions.</p>'
    meta.Session.add(page2)
    meta.Session.flush()
        
    log.info(_("Adding search page..."))
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
    
    log.info(_("Adding first post..."))
    post1 = model.Post()
    post1.title = u'First test post'
    post1.slug = u'first-test-post'
    post1.content = u'<p>This is the first test post</p>'
    post1.created_on = datetime.datetime(2008, 3, 17, 12, 30, 45)
    meta.Session.add(post1)
    meta.Session.flush()
    
    log.info(_("Adding fifth post..."))
    post5 = model.Post()
    post5.title = u'Fifth test post'
    post5.slug = u'fifth-test-post'
    post5.content = u'<p>This is the fifth test post</p>'
    post5.created_on = datetime.datetime(2008, 3, 17, 12, 30, 45)
    post5.draft = False
    post5.posted_on = datetime.datetime(2008, 3, 18, 12, 30, 45)
    meta.Session.add(post5)
    meta.Session.flush()
    
    log.info(_("Adding second post..."))
    post2 = model.Post()
    post2.title = u'Second test post'
    post2.slug = u'second-test-post'
    post2.content = u'<p>This is the second test post</p>'
    post2.created_on = datetime.datetime(2009, 3, 24, 12, 30, 45)
    post2.draft = False
    post2.posted_on = datetime.datetime(2009, 3, 24, 12, 30, 45)
    meta.Session.add(post2)
    meta.Session.flush()
    
    log.info(_("Adding third post..."))
    post3 = model.Post()
    post3.title = u'Third test post'
    post3.slug = u'third-test-post'
    post3.content = u'<p>This is the third test post</p>'
    post3.created_on = datetime.datetime(2009, 3, 25, 12, 30, 45)
    post3.draft = False
    post3.posted_on = datetime.datetime(2009, 3, 25, 12, 30, 45)
    meta.Session.add(post3)
    meta.Session.flush()
    
    log.info(_("Adding fourth post..."))
    post4 = model.Post()
    post4.title = u'Fourth test post'
    post4.slug = u'fourth-test-post'
    post4.content = u'<p>This is the fourth test post</p>'
    post4.created_on = datetime.datetime(2009, 4, 5, 12, 30, 45)
    post4.draft = False
    post4.posted_on = datetime.datetime(2009, 4, 5, 12, 30, 45)
    meta.Session.add(post4)
    meta.Session.flush()
    
    log.info(_("Adding second post comment..."))
    comment1 = model.Comment()
    comment1.post_id = int(2)
    comment1.content = u'This is my comment content'
    comment1.name = u'Responsible Web'
    comment1.email = u'nomail@gmail.com'
    comment1.url = u'http://responsibleweb.com'
    meta.Session.add(comment1)
    meta.Session.flush()
    
    log.info(_("Adding second post comment..."))
    comment2 = model.Comment()
    comment2.post_id = int(2)
    comment2.content = u'This is my second comment content'
    comment2.name = u'Responsible Web'
    comment2.email = u'nomail@gmail.com'
    comment2.url = u'http://responsibleweb.com'
    comment2.approved = True
    meta.Session.add(comment2)
    meta.Session.flush()
    
    log.info(_("Adding first tag..."))
    tag1 = model.Tag()
    tag1.name = u'Pylons'
    tag1.slug = u'pylons'
    meta.Session.add(tag1)
    meta.Session.flush()
    
    log.info(_("Adding second tag..."))
    tag2 = model.Tag()
    tag2.name = u'Python'
    tag2.slug = u'python'
    meta.Session.add(tag2)
    meta.Session.flush()
    
    log.info(_("Assigning tags..."))
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
