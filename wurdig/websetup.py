"""Setup the Wurdig application"""
import logging

from wurdig import model
from wurdig.config.environment import load_environment
from wurdig.model import meta

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup wurdig here"""
    load_environment(conf.global_conf, conf.local_conf)

    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
    
    log.info("Adding about page...")
    page = model.Page()
    page.title = u'About me and this site'
    page.slug = u'about'
    page.content = u"""
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
    meta.Session.add(page)
    meta.Session.commit()
    log.info('Successfully set up about page.')
    
    log.info("Adding teach page...")
    page = model.Page()
    page.title = u'My life as a teacher'
    page.slug = u'teaching'
    page.content = u"""
    I am often asked about my old teaching material (which used to be housed at http://www.my-classes.org - <a href="http://web.archive.org/web/20071216031655/http://www.my-classes.org/">wayback</a>).  <a href="http://jasonleveille.com/teacher/">My old lessons</a> are still available (I can't say how relevant they still are though!).  Let me know if you have any questions.
    """
    meta.Session.add(page)
    meta.Session.commit()
    log.info('Successfully set up teach page.')
