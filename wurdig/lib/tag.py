import helpers as h

__all__ = ['cloud', 'post_tags']

def cloud(tags):
    if len(tags):
        parts = []
        parts.append('<div class="hTagCloud"><ul class="popularity">')
        for tag in tags:
            parts.append('<li class="%s">' % tag_weight(tag.post_count));
            link_pattern = '<a href="%s" title="%s tagged with %s">%s</a>'
            url = h.url_for(controller='tag', 
                             action='archive', 
                             slug=tag.slug)
            parts.append(link_pattern % (url, 
                                         h.plural(tag.post_count, 'Post', 'Posts'), 
                                         tag.name, 
                                         tag.name)
            )
            parts.append('</li>')
        parts.append('</ul></div>')

    return '\n'.join(parts)
    
def post_tags(tags):
    
    return 'tags'

def tag_weight(count):
    classes = {'level_1' : 'popular', 
               'level_2' : 'v-popular',
               'level_3' : 'vv-popular',
               'level_4' : 'vvv-popular',
               'level_5' : 'vvvv-popular'}
    if count in range(0,1):
        return classes['level_1']
    elif count in range(2,3):
        return classes['level_2']
    elif count in range(16,20):
        return classes['level_3']
    elif count in range(21,30):
        return classes['level_4']
    elif count > 31:
        return classes['level_5']
    else:
        return ''