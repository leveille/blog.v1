from sqlalchemy.interfaces import ConnectionProxy
import time
 
import logging
log = logging.getLogger(__name__)
 
class TimerProxy(ConnectionProxy):
    def cursor_execute(self, execute, cursor, statement, parameters, context, executemany):
        now = time.time()
        try:
            return execute(cursor, statement, parameters, context)
        finally:
            total = time.time() - now
            log.debug("Query: %s" % statement)
            log.debug("Total Time: %f" % total)