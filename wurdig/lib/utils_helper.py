import glob, os, random
from time import gmtime

__all__ = ['random_header', 'mtime', 'abbr_datetime', 'ies_datetime']

def random_header():
    image = 'header2.jpg'
    try:
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = root + os.sep + 'public' + os.sep + 'images' \
                 + os.sep + 'headers' + os.sep
        images = glob.glob(path + '*.jpg')
        image = images.pop(random.randrange(len(images)))
        image = os.path.basename(image)        
    except Exception, e:
        pass
    return image

def mtime(abs_file_from_public):
    try:
        abs_public = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
            + os.sep + 'public'
        full_path = abs_public + abs_file_from_public
        return os.path.getmtime(full_path)
    except Exception, e:
        pass
    return 0

def abbr_datetime(datetime):
    d = ies_datetime(datetime)
    return '<abbr class="localize_datetime" title="%s">%s</abbr>' % (d, d) 

# http://tools.ietf.org/html/rfc2822.html
# a format for dates compatible with that specified in the 
# RFC 2822 Internet email standard.
def ies_datetime(datetime):
    try:
        return datetime.strftime('%a, %d %b %Y %H:%M:%S +0000')
    except Exception, e:
        pass
    return datetime