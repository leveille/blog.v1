import logging
import wurdig.lib.helpers as h
import wurdig.model as model
import wurdig.model.meta as meta

from pylons import cache, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators.cache import beaker_cache
from sqlalchemy.sql import and_
from webhelpers.feedgenerator import Atom1Feed
from wurdig.lib.base import BaseController

log = logging.getLogger(__name__)

class FeedController(BaseController):
    
    def redirect_wp_feeds(self):
        return redirect_to(controller='feed', action='posts_feed', _code=301)
        
    @beaker_cache(expire=28800, type='memory')
    def posts_feed(self):
        
        posts_q = meta.Session.query(model.Post).filter(
            model.Post.draft == False
        ).order_by([model.Post.posted_on.desc()]).limit(10)
        
        feed = Atom1Feed(
            title=config['blog.title'],
            subtitle=config['blog.subtitle'],
            link=u"http://%s" % request.environ['HTTP_HOST'],
            description=u"Most recent posts for %s" % config['blog.title'],
            language=u"en",
        )
        
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
                categories=tuple(tags)
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
    @beaker_cache(expire=3600, type='memory')
    def comments_feed(self):   
        comments_q = meta.Session.query(model.Comment).filter(model.Comment.approved==True)
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(20)
        
        feed = Atom1Feed(
            title=u"Comments for " + h.wurdig_title(),
            subtitle=h.wurdig_subtitle(),
            link=u"http://%s" % request.environ['HTTP_HOST'],
            description=h.wurdig_subtitle(),
            language=u"en",
        )
        
        for comment in comments_q:
            post_q = meta.Session.query(model.Post)
            c.post = comment.post_id and post_q.filter_by(id=int(comment.post_id)).first() or None
            if c.post is not None:
                feed.add_item(
                    title=u"Comment on %s" % c.post.title,
                    link=u'http://%s%s' % (request.environ['HTTP_HOST'], h.url_for(
                        controller='post', 
                        action='view', 
                        year=c.post.posted_on.strftime('%Y'), 
                        month=c.post.posted_on.strftime('%m'), 
                        slug=c.post.slug,
                        anchor=u"comment-" + str(comment.id)
                    )),
                    description=comment.content
                )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
    @beaker_cache(expire=14400, type='memory', query_args=True)
    def post_comment_feed(self, post_id=None):
        if post_id is None:
            abort(404)
        
        post_q = meta.Session.query(model.Post)
        c.post = post_id and post_q.filter(and_(model.Post.id==int(post_id), 
                                                model.Post.draft==False)).first() or None
        if c.post is None:
            abort(404)
        comments_q = meta.Session.query(model.Comment).filter(and_(model.Comment.post_id==c.post.id, 
                                                                   model.Comment.approved==True))
        comments_q = comments_q.order_by(model.comments_table.c.created_on.desc()).limit(10)
        
        feed = Atom1Feed(
            title=h.wurdig_title() + u' - ' + c.post.title,
            subtitle=u'Most Recent Comments',
            link=u'http://%s%s' % (request.environ['HTTP_HOST'], h.url_for(
                    controller='post', 
                    action='view', 
                    year=c.post.posted_on.strftime('%Y'), 
                    month=c.post.posted_on.strftime('%m'), 
                    slug=c.post.slug
                )),
            description=u"Most recent comments for %s" % c.post.title,
            language=u"en",
        )
        
        for comment in comments_q:
            feed.add_item(
                title=c.post.title + u" comment #%s" % comment.id,
                link=u'http://%s%s' % (request.environ['HTTP_HOST'], h.url_for(
                    controller='post', 
                    action='view', 
                    year=c.post.posted_on.strftime('%Y'), 
                    month=c.post.posted_on.strftime('%m'), 
                    slug=c.post.slug,
                    anchor=u'comment-' + str(comment.id)
                )),
                description=comment.content
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
    @beaker_cache(expire=28800, type='memory', query_args=True)
    def tag_feed(self, slug=None):
        if slug is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        c.tag = tag_q.filter(model.Tag.slug==slug).first()
        
        if(c.tag is None):
            c.tagname = slug
        else:
            c.tagname = c.tag.name
            
        posts_q = meta.Session.query(model.Post).filter(
            and_(
                 model.Post.tags.any(slug=slug), 
                 model.Post.draft == False 
            )
        ).order_by([model.Post.posted_on.desc()]).limit(10)

        feed = Atom1Feed(
            title=config['blog.title'],
            subtitle=u'Blog posts tagged "%s"' % slug,
            link=u"http://%s%s" % (request.environ['HTTP_HOST'], h.url_for(
                controller='tag',
                action='archive',
                slug=slug
            )),
            description=u"Blog posts tagged %s" % slug,
            language=u"en",
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
                description=post.content,
                categories=tuple(tags)
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
