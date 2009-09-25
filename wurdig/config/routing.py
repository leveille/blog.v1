"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'], explicit=True)
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('/', controller='post', action='home')
    
    map.connect('/feeds/', 
                controller='feed', 
                action='redirect_wp_feeds')
    
    map.connect('/feeds/blog', 
                controller='feed', 
                action='posts_feed')
    
    map.connect('/feeds/blog/sitemap', 
                controller='feed', 
                action='posts_feed_sitemap')
    
    map.connect('/feeds/pages/sitemap', 
                controller='feed', 
                action='pages_feed_sitemap')
    
    map.connect('/feeds/comments', 
                controller='feed', 
                action='comments_feed')
    
    map.connect('/feeds/comments/{post_id}',
                controller='feed',
                action='post_comment_feed',
                requirements = dict(post_id='\d+')
    )

    map.connect('/feeds/tag/{slug}',
                controller='feed',
                action='tag_feed',
                requirements = dict(slug='[-\w]+')
    )
    
    map.connect('/post/{post_id}/{controller}/{action}',
                requirements = dict(post_id='\d+')
    ) 
    
    map.connect('/post/{post_id}/{controller}/{action}/{id}',
                requirements = dict(post_id='\d+', id='\d+')
    )
    
    map.connect('/{year}/{month}/{slug}', controller='post', 
                action='view', 
                requirements = {'year' : '\d{2,4}', 
                                'month' : '\d{1,2}', 
                                'slug' : '[-\w]+'})
    
    map.redirect('/{year}/{month}/{slug}/', '/{year}/{month}/{slug}', _redirect_code='301 Moved Permanently')
    
    map.connect('/{year}/{month}', controller='post', 
                action='archive', 
                requirements = {'year' : '\d{2,4}', 'month' : '\d{1,2}'})
    
    map.connect('/{year}', controller='post', 
                action='archive', 
                requirements = {'year' : '\d{2,4}'})
    
    map.connect('/category/{slug}', controller='tag', 
                action='category', 
                requirements = {'slug' : '[-\w]+'})
    
    # Not a big fan of hardcoding in these actions,
    # but I'm unsure how to proceed otherwise in order to get
    # a nice clean url for the tag slug
    map.connect('/tag/{action}', controller='tag', 
                requirements = {'action' : 'cloud|new|create|edit|save|list|delete'})
    
    map.connect('/tag/{slug}', controller='tag', 
                action='archive', 
                requirements = {'slug' : '[-\w]+'})
    
    map.connect('/{slug}', controller='page', 
                action='view', 
                requirements = {'slug' : '[-\w]+'})
    
    map.redirect('/{slug}/', '/{slug}', _redirect_code='301 Moved Permanently')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
