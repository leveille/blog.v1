import helpers as h
from pylons import tmpl_context as c
from pylons.i18n.translation import _
from wurdig import model
from wurdig.model import meta

__all__ = ['post_tags']

def cloud():
    # grab tag list and x recent comments for display in sidebar
    tags_q = meta.Session.query(model.Tag)
    c.tags = tags_q.all()
    if len(c.tags):
        parts = []
        parts.append('<div class="hTagCloud"><h4>%s</h4><ul class="popularity">' % _('Tags'))
        for tag in c.tags:
            parts.append('<li class="%s">' % tag_weight(tag.post_count));
            link_pattern = '<a href="%s" rel="tag" title="%s %s %s">%s</a>'
            url = h.url_for(controller='tag', 
                             action='archive', 
                             slug=tag.slug)
            parts.append(link_pattern % (url, 
                                         h.plural(tag.post_count, _('Post'), _('Posts')), 
                                         _('tagged'),
                                         tag.name, 
                                         tag.name)
            )
            parts.append('</li>')
        parts.append('</ul></div>')

    return '\n'.join(parts)

def post_tags(tags):
    if len(tags):
        parts, _tags = [], []
        parts.append('<span class="wurdig-entry-tags">')
        parts.append('<strong>%s</strong> : ' % _('Tagged in'))
        for tag in tags:
            link_pattern = '<a href="%s" rel="tag">%s</a>'
            _tags.append(link_pattern % (h.url_for(controller='tag', action='archive', slug=tag.slug),
                                         tag.name
                                         ))
        tags = ', '.join(_tags)
        parts.append(tags)
        parts.append('</span>')

    return '\n'.join(parts)

def tag_weight(count):
    classes = {'level_1' : 'popular', 
               'level_2' : 'v-popular',
               'level_3' : 'vv-popular',
               'level_4' : 'vvv-popular',
               'level_5' : 'vvvv-popular'}
    if count in range(1,6):
        return classes['level_1']
    elif count in range(7,15):
        return classes['level_2']
    elif count in range(16,22):
        return classes['level_3']
    elif count in range(23,30):
        return classes['level_4']
    elif count > 31:
        return classes['level_5']
    else:
        return ''