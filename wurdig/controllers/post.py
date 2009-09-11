import datetime as d
import formencode
import logging
import re
import webhelpers.paginate as paginate
import wurdig.lib.helpers as h
import wurdig.model as model
import wurdig.model.meta as meta

from authkit.authorize.pylons_adaptors import authorize
from formencode import htmlfill
from pylons import app_globals, config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from pylons.i18n.translation import _
from sqlalchemy.sql import and_, delete
from wurdig.lib.base import BaseController, Cleanup, ConstructSlug, render

log = logging.getLogger(__name__)

class UniqueSlug(formencode.FancyValidator):
    messages = {
        'invalid': _(u'Slug must be unique.')
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = formencode.validators.UnicodeString(max=100).to_python(value, state)
        # validate that slug only contains letters, numbers, and dashes
        result = re.compile("[^\w-]").search(value)
        if result:
            raise formencode.Invalid(_("Slug can only contain "
                                       "letters, numbers, and dashes."), value, state)
        
        # Ensure slug is unique
        post_q = meta.Session.query(model.Post).filter_by(slug=value)
        if request.urlvars['action'] == 'save':
            # we're editing an existing post.
            post_q = post_q.filter(model.Post.id != int(request.urlvars['id']))
            
        # Check if the slug exists
        slug = post_q.first()
        if slug is not None:
            raise formencode.Invalid(
                self.message('invalid', state),
                value, state)
        
        return value
    
class ValidTags(formencode.FancyValidator):
    messages = {
        'invalid': _("One ore more selected tags could not "
                     "be found in the database.")
    }
    def _to_python(self, values, state):
        all_tag_ids = [tag.id for tag in meta.Session.query(model.Tag)]
        for tag_id in values['tags']:
            if tag_id not in all_tag_ids:
                raise formencode.Invalid(
                    self.message('invalid', state),
                    values, state
                )
        return values

class NewPostForm(formencode.Schema):
    pre_validators = [ConstructSlug(), Cleanup()]
    allow_extra_fields = True
    filter_extra_fields = True
    title = formencode.validators.UnicodeString(
        not_empty=True,
        max=100, 
        messages={
            'empty': _('Enter a post title.')
        },
        strip=True
    )
    slug = UniqueSlug(
        not_empty=True, 
        messages={
            'empty': _('Enter a post slug, ex: my-post-title.')
        },
        max=100, 
        strip=True
    )
    content = formencode.validators.UnicodeString(
        not_empty=True,
        messages={
            'empty': _('Enter some post content.')
        },
        strip=True
    )
    draft = formencode.validators.StringBool(if_missing=False)
    comments_allowed = formencode.validators.StringBool(if_missing=False)
    tags = formencode.foreach.ForEach(formencode.validators.Int())
    chained_validators = [ValidTags()]

class PostController(BaseController):
    
    def home(self): 
        @app_globals.cache.region('short_term', 'post.home.load_page')
        def load_page(page):
            return paginate.Page(
                meta.Session.query(model.Post).filter(
                    model.Post.draft == False
                ),
                page=page,
                items_per_page = 10,
                controller='post',
                action='home'
            )
            
        try:
            c.page = int(request.params.get('page', 1))
            c.paginator = load_page(c.page)
        except:
            abort(400)
            
        return render('/derived/post/home.html')
    
    def archive(self, year=None, month=None):  
         
        try:
            year_i = int(year)
        except:
            abort(400)
        
        (c.date, month_start, month_end, day_end) = (year, 1, 12, 31)
        
        if month is not None:
            try:
                month_i = int(month)
            except:
                abort(400)
            
            import calendar
            c.date = calendar.month_name[month_start] + ', ' + year
            (month_start, month_end) = (month_i, month_i)
            day_end = calendar.monthrange(year_i, month_start)[1]
        
        @app_globals.cache.region('short_term', 'post.archive.load_page')
        def load_page(page):
            posts_q = meta.Session.query(model.Post).filter(
                and_(
                    model.Post.posted_on >= d.datetime(year_i, month_start, 1), 
                    model.Post.posted_on <= d.datetime(year_i, month_end, day_end), 
                    model.Post.draft == False
                )
            )
            return paginate.Page(
                posts_q,
                page=page,
                items_per_page = 10,
                controller='post',
                action='archive',
                year=year,
                month=month,
            )
            
        try:
            c.paginator = load_page(int(request.params.get('page', 1)))
        except:
            abort(400)
                    
        return render('/derived/post/archive.html')
    
    def view(self, year, month, slug):        
        @app_globals.cache.region('short_term', 'post.view.load_post')
        def load_post(year, month, slug):
            import calendar
            return meta.Session.query(model.Post).filter(
                and_(model.Post.posted_on >= d.datetime(year, month, 1), 
                     model.Post.posted_on <= d.datetime(year, month, calendar.monthrange(year, month)[1]),
                     model.Post.draft == False,
                     model.Post.slug == slug)
            ).first()

        try:
            c.post = load_post(int(year), int(month), slug)
        except:
            abort(400)
                                 
        if c.post is None:
            abort(404)
            
        return h.comment_form('/derived/post/view.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def new(self):
        tag_q = meta.Session.query(model.Tag)
        c.available_tags = [(tag.id, tag.name) for tag in tag_q]
        return render('/derived/post/new.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewPostForm(), form='new')
    def create(self):
        post = model.Post()
        
        tags = self.form_result['tags']
        del self.form_result['tags']
        
        for k, v in self.form_result.items():
            setattr(post, k, v)
        
        if not post.draft:
            post.posted_on = d.datetime.utcnow()
        
        post.created_on = d.datetime.utcnow()
        
        meta.Session.add(post)

        for tag in tags:
            t = meta.Session.query(model.Tag).get(tag)
            post.tags.append(t)
        
        meta.Session.commit()        
        session['flash'] = _('Post successfully added.')
        session.save()
                
        # Issue an HTTP redirect
        if post.posted_on is not None:
            return redirect_to(controller='post', 
                               action='view', 
                               year=post.posted_on.strftime('%Y'), 
                               month=post.posted_on.strftime('%m'), 
                               slug=post.slug)
        else:
            return redirect_to(controller='post', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
            
        try:
            id = int(id)
        except:
            abort(400)
            
        post_q = meta.Session.query(model.Post)
        c.post = post_q.filter_by(id=id).first()
        if c.post is None:
            abort(404)
        
        tag_q = meta.Session.query(model.Tag)
        c.available_tags = [(tag.id, tag.name) for tag in tag_q]
        c.selected_tags = [str(tag.id) for tag in c.post.tags]
        
        values = {
            'id':c.post.id,
            'title':c.post.title,
            'slug':c.post.slug,
            'content':c.post.content,
            'draft':c.post.draft,
            'comments_allowed':c.post.comments_allowed,
            'tags':c.selected_tags
        }
        return htmlfill.render(render('/derived/post/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewPostForm(), form='edit')
    def save(self, id=None):

        try:
            id = int(id)
        except:
            abort(400)
            
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
            
        posted_tags = self.form_result['tags']
        del self.form_result['tags']
            
        for k,v in self.form_result.items():
            if getattr(post, k) != v:
                setattr(post, k, v)
                
        # is this post marked draft or not
        if post.draft:
            post.posted_on = None
        elif post.posted_on is None:
            post.posted_on = d.datetime.utcnow()
        
        # remove existing tags which were not selected
        # in the "posted" tags
        for i, tag in enumerate(post.tags):
            if tag.id not in posted_tags:
                del post.tags[i]
        
        # let's add the new tags for this post
        tagids = [tag.id for tag in post.tags]
        for tag in posted_tags:
            if tag not in tagids:
                t = meta.Session.query(model.Tag).get(tag)
                post.tags.append(t)
            
        meta.Session.commit()
        session['flash'] = _('Post successfully updated.')
        session.save()

        if not post.draft:
            return redirect_to(controller='post', 
                               action='view', 
                               year=post.posted_on.strftime('%Y'), 
                               month=post.posted_on.strftime('%m'), 
                               slug=post.slug)
        else:
            return redirect_to(controller='post', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        posts_q = meta.Session.query(model.Post).order_by([model.Post.draft.desc(),model.Post.posted_on.desc()])
        
        try:
            posts_page = int(request.params.get('posts_page', 1))
        except:
            abort(400)
        
        c.paginator = paginate.Page(
            posts_q,
            page=posts_page,
            items_per_page = 15,
            controller='post',
            action='list',
        )
        return render('/derived/post/list.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def delete_confirm(self, id=None):

        try:
            id = int(id)
        except:
            abort(400)
            
        post_q = meta.Session.query(model.Post)
        c.post = post_q.filter_by(id=id).first()
        if c.post is None:
            abort(404)
        return render('/derived/post/delete_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):

        try:
            id = int(request.params.getone('id'))
        except:
            abort(400)
        
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
        # delete tags and comments associated with post
        meta.Session.execute(delete(model.poststags_table, model.poststags_table.c.post_id==post.id))
        meta.Session.execute(delete(model.comments_table, model.comments_table.c.post_id==post.id))
        meta.Session.delete(post)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'%s'}" % _('The post has been deleted')
        else:
            session['flash'] = _('Post successfully deleted.')
            session.save()
            return redirect_to(controller='post', action='list')
