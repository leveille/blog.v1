import helpers as h
from formencode import htmlfill
from pylons.i18n.translation import _
from wurdig import model
from wurdig.model import meta
from wurdig.lib.base import render

__all__ = ['comment_form', 'comment_filter', 'recent_comments']

def comment_form(template):
    rememberme_values = h.get_rememberme_cookie()
    if rememberme_values is not None:    
        return htmlfill.render(render(template), rememberme_values)
    return render(template)

def comment_filter(comment):
    return h.sanitize_html(comment)

def recent_comments():
    comments_q = meta.Session.query(model.Comment).filter(model.Comment.approved==True)
    comments_q = comments_q.order_by(model.comments_table.c.created_on.desc())
    recent_comments = comments_q.join(model.Post).limit(4)
    if recent_comments is None:
        return ''
    else:
        comments= []
        template = """
        <div id="wurdig-recent-comments" class="wurdig-sidebar-list">
            <h4>%s</h4>
            <ul>
                %s
            </ul>
        </div>
        """

        for comment in recent_comments:
            i = """
                <li class="%s">
                    <span class="lone">%s shared: </span>
                    <span>%s</span>
                    <span>%s: %s</span>
                </li>
            """
            name = comment.name
            if comment.url is not None:
                name = h.link_to(comment.name, comment.url)
            
            content = h.truncate(h.strip_tags(comment.content), 80)
                             
            link = h.link_to(
                comment.posts.title,
                h.url_for(
                    controller='post', 
                    action='view', 
                    year=comment.posts.posted_on.strftime('%Y'), 
                    month=comment.posts.posted_on.strftime('%m'), 
                    slug=comment.posts.slug,
                    anchor=u"comment-" + str(comment.id)
                )
            )
            comments.append(i % (comment.id, name, content, _('Shared in'), link))
        return template % (_('Newest Comments'), '\n'.join(comments))
    