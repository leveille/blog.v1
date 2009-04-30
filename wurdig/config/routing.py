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
    
    map.connect('/feed/{format}', 
                controller='post', 
                action='feed', 
                requirements = dict(format='atom'))
    
    map.connect('/comments/feed', 
                controller='comment', 
                action='feed')
    
    map.connect('/post/{post_id}/{controller}/{action}',
                requirements = dict(post_id='\d+')
    ) 
    
    map.connect('/post/{post_id}/{controller}/{action}/{id}',
                requirements = dict(post_id='\d+', id='\d+')
    )
    
    map.connect('/post/{post_id}/{controller}/pfeed/{format}',
                action='pfeed',
                requirements = dict(post_id='\d+', format='atom')
    )
    
    map.connect('/{year}/{month}/{slug}', controller='post', 
                action='view', 
                requirements = {'year' : '\d{2,4}', 
                                'month' : '\d{1,2}', 
                                'slug' : '[-\w]+'})
    
    map.connect('/{year}/{month}', controller='post', 
                action='archive', 
                requirements = {'year' : '\d{2,4}', 'month' : '\d{1,2}'})
    
    map.connect('/{year}', controller='post', 
                action='archive', 
                requirements = {'year' : '\d{2,4}'})
    
    # Not a big fan of hardcoding in these actions,
    # but I'm unsure how to proceed otherwise in order to get
    # a nice clean url for the tag slug
    map.connect('/tag/{action}', controller='tag', 
                requirements = {'action' : 'new|create|edit|save|list|delete'})
    
    map.connect('/tag/{slug}', controller='tag', 
                action='archive', 
                requirements = {'slug' : '[-\w]+'})
    
    map.connect('/{slug}', controller='page', 
                action='view', 
                requirements = {'slug' : '[-\w]+'})

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
