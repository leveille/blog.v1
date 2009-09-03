import logging
import wurdig.lib.helpers as h
import wurdig.model as model
import wurdig.model.meta as meta

from pylons import app_globals, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.i18n.translation import _
from sqlalchemy.sql import and_
from webhelpers.feedgenerator import Atom1Feed
from wurdig.lib.base import BaseController

log = logging.getLogger(__name__)

class FeedController(BaseController):
    
    def redirect_wp_feeds(self):
        return redirect_to(controller='feed', action='posts_feed', _code=301)
        
    def posts_feed(self):        
        @app_globals.cache.region('long_term')
        def load_posts():
            feed = Atom1Feed(
                title=h.wurdig_title(),
                subtitle=h.wurdig_subtitle(),
                link=u'http://%s' % request.environ['HTTP_HOST'],
                description=_(u"Most recent posts for %s") % h.wurdig_title(),
                language=u'en',
            )
            
            posts_q = meta.Session.query(model.Post).filter(
                model.Post.draft == False
            ).order_by([model.Post.posted_on.desc()]).limit(10)
        
            for post in posts_q:
                tags = [tag.name for tag in post.tags]
                feed.add_item(
                    title=post.title,
                    link=u'http://%s%s' % (request.environ['HTTP_HOST'], h.url_for(
                        controller='post', 
                        action='view', 
                        year=post.posted_on.strftime('%Y'), 
                        month=post.posted_on.strftime('%m'), 
                        slug=post.slug
                    )),
                    description=post.content,
                    pubdate=post.posted_on,
                    categories=tuple(tags)
                )
            return feed.writeString('utf-8')
        
        feed = load_posts()
        response.content_type = 'application/atom+xml'
        return feed
    
    def comments_feed(self):
        @app_globals.cache.region('medium_term', 'comments_feed')
        def load_comments():
            feed = Atom1Feed(
                title=_(u'Comments for %s') % h.wurdig_title(),
                subtitle=h.wurdig_subtitle(),
                link=u'http://%s' % request.environ['HTTP_HOST'],
                description=h.wurdig_subtitle(),
                language=u'en',
            )
            comments_q = meta.Session.query(model.Comment).filter(model.Comment.approved==True)
            comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(20)
        
            comment_meta = u"""
            <p style="margin: 0px; padding: 5px 15px 5px 15px; border: 1px solid #000">
            %s %s</p>
            """ % (_('Posted in'), '<a href="%s">%s</a>')
            
            for comment in comments_q:
                post_q = meta.Session.query(model.Post)
                c.post = comment.post_id and post_q.filter_by(id=int(comment.post_id)).first() or None
                if c.post is not None:
                    post_link=u'http://%s%s' % (request.environ['HTTP_HOST'], h.url_for(
                        controller='post', 
                        action='view', 
                        year=c.post.posted_on.strftime('%Y'), 
                        month=c.post.posted_on.strftime('%m'), 
                        slug=c.post.slug
                    ))
                    comment_link=post_link + u"#comment-" + str(comment.id)
                    feed.add_item(
                        title=u'Comment from %s' % comment.name,
                        link=comment_link,
                        unique_id=comment_link,
                        author_name=comment.name,
                        author_link=comment.url,
                        pubdate=comment.created_on,
                        description=comment.content + comment_meta % (post_link, c.post.title)
                    )
            return feed.writeString('utf-8')
        
        feed = load_comments()
        response.content_type = 'application/atom+xml'
        return feed

    def post_comment_feed(self, post_id=None):
        
        try:
            post_id = int(post_id)
        except:
            abort(400)
        
        @app_globals.cache.region('medium_term', 'post_comments_feed')
        def load_comments(post_id):
            post_q = meta.Session.query(model.Post)
            c.post = post_id and post_q.filter(and_(model.Post.id==int(post_id), 
                                                    model.Post.draft==False)).first() or None
            if c.post is None:
                abort(404)
            comments_q = meta.Session.query(model.Comment).filter(and_(model.Comment.post_id==int(c.post.id), 
                                                                       model.Comment.approved==True))
            comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(10)
            
            feed = Atom1Feed(
                title=h.wurdig_title() + u' - ' + c.post.title,
                subtitle=_(u'Most Recent Comments'),
                link=u'http://%s%s' % (request.environ['HTTP_HOST'], h.url_for(
                        controller='post', 
                        action='view', 
                        year=c.post.posted_on.strftime('%Y'), 
                        month=c.post.posted_on.strftime('%m'), 
                        slug=c.post.slug
                    )),
                description=_(u'Most recent comments for %s') % c.post.title,
                language=u'en',
            )
            
            comment_meta = u"""
            <p style="margin: 0px; padding: 5px 15px 5px 15px; border: 1px solid #000">
            %s %s</p>
            """ % (_('Posted in'), '<a href="%s">%s</a>')
            
            for comment in comments_q:
                post_link=u'http://%s%s' % (request.environ['HTTP_HOST'], h.url_for(
                    controller='post', 
                    action='view', 
                    year=c.post.posted_on.strftime('%Y'), 
                    month=c.post.posted_on.strftime('%m'), 
                    slug=c.post.slug
                ))
                comment_link=post_link + u'#comment-' + str(comment.id)
                
                feed.add_item(
                    title=_(u'Comment from %s') % comment.name,
                    link=comment_link,
                    unique_id=comment_link,
                    author_name=comment.name,
                    author_link=comment.url,
                    pubdate=comment.created_on,
                    description=comment.content + comment_meta % (post_link, c.post.title)
                )
            return feed.writeString('utf-8')
        
        feed = load_comments(post_id)
        response.content_type = 'application/atom+xml'
        return feed
    
    def tag_feed(self, slug=None):
        if slug is None:
            abort(404)
            
        @app_globals.cache.region('long_term', 'load_tag')
        def load_tag(slug): 
            tag_q = meta.Session.query(model.Tag)
            tag = tag_q.filter(model.Tag.slug==slug).first()
            return tag
        
        c.tag = load_tag(slug)
        if(c.tag is None):
            abort(404)
        c.tagname = c.tag.name
        
        @app_globals.cache.region('long_term', 'load_tag_posts')
        def load_tag_posts(slug):                
            posts_q = meta.Session.query(model.Post).filter(
                and_(
                     model.Post.tags.any(slug=slug), 
                     model.Post.draft == False 
                )
            ).order_by([model.Post.posted_on.desc()]).limit(10)
    
            feed = Atom1Feed(
                title=h.wurdig_title(),
                subtitle=_(u'Blog posts tagged "%s"') % slug,
                link=u"http://%s%s" % (request.environ['HTTP_HOST'], h.url_for(
                    controller='tag',
                    action='archive',
                    slug=slug
                )),
                description=_(u'Blog posts tagged %s') % slug,
                language=u'en',
            )
            
            for post in posts_q:
                tags = [tag.name for tag in post.tags]
                feed.add_item(
                    title=post.title,
                    link=u'http://%s%s' % (request.server_name, h.url_for(
                        controller='post', 
                        action='view', 
                        year=post.posted_on.strftime('%Y'), 
                        month=post.posted_on.strftime('%m'), 
                        slug=post.slug
                    )),
                    pubdate=post.posted_on,
                    description=post.content,
                    categories=tuple(tags)
                )
            return feed.writeString('utf-8')
        
        feed = load_tag_posts(slug)
        response.content_type = 'application/atom+xml'
        return feed
