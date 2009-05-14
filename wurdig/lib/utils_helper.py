import glob, os, random

__all__ = ['random_header']

def random_header():
    image = 'header1.jpg'
    try:
        path = os.getcwd() + os.sep + 'wurdig' + os.sep + 'public' \
                + os.sep + 'images' + os.sep + 'headers' + os.sep
        images = glob.glob(path + '*.jpg')
        import pprint
        image = images.pop(random.randrange(len(images)))
        image = os.path.basename(image)        
    except Exception, e:
        pass
    return image