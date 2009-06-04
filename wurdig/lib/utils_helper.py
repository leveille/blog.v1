import glob, os, random

__all__ = ['random_header', 'mtime']

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

def mtime(rel_file_path_from_public_dir):
    try:
        doc_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) \
            + os.sep + 'public'
        full_file_path = doc_root + rel_file_path_from_public_dir
        return os.path.getmtime(full_file_path)
    except Exception, e:
        pass
    return 0
