from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

"""The application's Globals object"""

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """
        cache_opts = {
            'cache.data_dir':'/tmp/cache/data',
            'cache.lock_dir':'/tmp/cache/lock',
            'cache.regions':'short_term, long_term, medium_term',
            'cache.short_term.type':'memory',
            'cache.short_term.expire':'3600',
            'cache.medium_term.type':'file',
            'cache.medium_term.expire':'28800',
            'cache.long_term.type':'file',
            'cache.long_term.expire':'86400',
        }
        self.cache = CacheManager(**parse_cache_config_options(cache_opts))
