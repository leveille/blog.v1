import calendar
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
from pylons import config, request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from sqlalchemy.sql import and_, delete
from webhelpers.feedgenerator import Atom1Feed
from wurdig.lib.base import BaseController, Cleanup, ConstructSlug, render

log = logging.getLogger(__name__)

class UniqueSlug(formencode.FancyValidator):
    messages = {
        'invalid': 'Slug must be unique'
    }
    def _to_python(self, value, state):
        # Ensure we have a valid string
        value = formencode.validators.UnicodeString(max=100).to_python(value, state)
        # validate that slug only contains letters, numbers, and dashes
        result = re.compile("[^\w-]").search(value)
        if result:
            raise formencode.Invalid("Slug can only contain letters, numbers, and dashes", value, state)
        
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
        'invalid': 'One ore more selected tags could not ' +
        'be found in the database'
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
            'empty':'Enter a post title'
        },
        strip=True
    )
    slug = UniqueSlug(not_empty=True, max=100, strip=True)
    content = formencode.validators.UnicodeString(
        not_empty=True,
        messages={
            'empty':'Enter some post content.'
        },
        strip=True
    )
    draft = formencode.validators.StringBool(if_missing=False)
    comments_allowed = formencode.validators.StringBool(if_missing=False)
    tags = formencode.foreach.ForEach(formencode.validators.Int())
    chained_validators = [ValidTags()]

class PostController(BaseController):
    
    def home(self):
        posts_q = meta.Session.query(model.Post).filter(
            model.Post.draft == False
        )
        c.paginator = paginate.Page(
            posts_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='post',
            action='home'
        )      
        return render('/derived/post/home.html')
        
    def feeds(self):
        
        posts_q = meta.Session.query(model.Post).filter(
            model.Post.draft == False
        ).order_by([model.Post.posted_on.desc()]).limit(10)
        
        feed = Atom1Feed(
            title=config['blog.title'],
            subtitle=config['blog.subtitle'],
            link=u"http://%s" % request.server_name,
            description=u"Most recent posts for %s" % config['blog.title'],
            language=u"en",
        )
        
        for post in posts_q:
            feed.add_item(
                title=post.title,
                link=h.url_for(
                    controller='post', 
                    action='view', 
                    year=post.posted_on.strftime('%Y'), 
                    month=post.posted_on.strftime('%m'), 
                    slug=post.slug
                ),
                description=h.chop_at(post.content, '<!--more-->'),
                # Why can't I do a tuple of post.tags here?
                # categories=tuple(post.tags)
                categories=()
            )
                
        response.content_type = 'application/atom+xml'
        return feed.writeString('utf-8')
    
    def archive(self, year=None, month=None):   
        if year is None:
            abort(404)
        
        (c.date, year_i, month_start, month_end, day_end) = (year, int(year), 1, 12, 31)
        
        if month is not None:
            c.date = calendar.month_name[month_start] + ', ' + year
            (month_start, month_end) = (int(month), int(month))
            day_end = calendar.monthrange(year_i, month_start)[1]
        
        posts_q = meta.Session.query(model.Post).filter(
            and_(
                model.Post.posted_on >= d.datetime(year_i, month_start, 1), 
                model.Post.posted_on <= d.datetime(year_i, month_end, day_end), 
                model.Post.draft == False
            )
        )
        
        c.paginator = paginate.Page(
            posts_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='post',
            action='archive',
            year=year,
            month=month,
        )
                
        return render('/derived/post/archive.html')
    
    def view(self, year, month, slug):
        (year_i, month_i) = (int(year), int(month))
        c.post = meta.Session.query(model.Post).filter(
            and_(model.Post.posted_on >= d.datetime(year_i, month_i, 1), 
                 model.Post.posted_on <= d.datetime(year_i, month_i, calendar.monthrange(year_i, month_i)[1]),
                 model.Post.draft == False,
                 model.Post.slug == slug)
        ).first()
                                 
        if c.post is None:
            abort(404)
            
        return render('/derived/post/view.html')
    
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
            post.posted_on = d.datetime.now()
        
        meta.Session.add(post)

        for tag in tags:
            t = meta.Session.query(model.Tag).get(tag)
            post.tags.append(t)
            
        meta.Session.commit()
        session['flash'] = 'Post successfully added.'
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
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_q.filter_by(id=id).first()
        if c.post is None:
            abort(404)
        import pprint
        
        tag_q = meta.Session.query(model.Tag)
        c.available_tags = [(tag.id, tag.name) for tag in tag_q]
        c.selected_tags = [str(tag.id) for tag in c.post.tags]
        
        values = {
            'id':c.post.id,
            'title':c.post.title,
            'slug':c.post.slug,
            ## Setting errors to replace
            ## App failing w/ content not properly encoded
            ## post WP import.  This will hopefully only be
            ## a temporary solution
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
        if id is None:
            abort(404)
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
        # this check for not post.draft is not necessary, but it is more readable
        elif not post.draft and post.posted_on is None:
            post.posted_on = d.datetime.now()
        
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
        session['flash'] = 'Post successfully updated.'
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
        c.paginator = paginate.Page(
            posts_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 50,
            controller='post',
            action='list',
        )
        return render('/derived/post/list.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):
        # @todo: delete confirmation
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
        meta.Session.execute(delete(model.poststags_table, model.poststags_table.c.post_id==post.id))
        meta.Session.delete(post)
        meta.Session.commit()
        session['flash'] = 'Post successfully deleted.'
        session.save()
        return redirect_to(controller='post', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def delete_confirm(self, id=None):
        if id is None:
            abort(404)
        post_q = meta.Session.query(model.Post)
        c.post = post_q.filter_by(id=id).first()
        if c.post is None:
            abort(404)
        return render('/derived/post/delete_confirm.html')

    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    def delete(self, id=None):
        id = request.params.getone('id')
        post_q = meta.Session.query(model.Post)
        post = post_q.filter_by(id=id).first()
        if post is None:
            abort(404)
        meta.Session.delete(post)
        meta.Session.commit()
        if request.is_xhr:
            response.content_type = 'application/json'
            return "{'success':true,'msg':'The post has been deleted'}"
        else:
            session['flash'] = 'Post successfully deleted.'
            session.save()
            return redirect_to(controller='post', action='list')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def scrape(self):
        from BeautifulSoup import BeautifulSoup
        import re, urllib2, sys
        """
        Used to scrape post markup from wp site
        This is post wp xml import.  Used really only for the purpose
        of gathering markup
        """
        posts_q = meta.Session.query(model.Post).filter(
            model.Post.draft == False
        ).all()
        
        # for debugging, write to file
        f = open('/home/leveille/development/python/pylons/Wurdig/posts.txt', 'a')
        for post in posts_q:
            f.write('\n++++++++++++++++++++++++++++++++\n')
            try:
                year = str(post.posted_on.strftime('%Y'))
                month = str(post.posted_on.strftime('%m'))
                slug = post.slug
                url = 'http://jasonleveille.com/%s/%s/%s' % (year, month, slug)
                response = urllib2.urlopen(url)
                html = response.read()
                soup = BeautifulSoup(html)
                
                subtree = soup.find('div', { "class" : "entry" }).findAll('p')[-1]
                subtree.extract()

                text = soup.find('div', { "class" : "entry" })
                text = text.encode('utf-8')
                text = h.mytidy(text)
                
                f.write(text)
                
                # if all seems fine, uncomment and write to database
                post.content = text
                meta.Session.add(post)
                meta.Session.commit()
            except Exception, e:
                print '\nFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\n';
                import pprint
                pprint.pprint(e)
                f.write('Exception: ')
                print '\nFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF\n';
            
            f.write('\n++++++++++++++++++++++++++++++++\n')
        f.close()
        response.content_type = 'text/plain'
        return 'done'
    
    @h.auth.authorize(h.auth.is_valid_user)
    def replace(self):
        posts_q = meta.Session.query(model.Post).all()
        
        for post in posts_q:
            try:
                post.content = post.content.replace('wp-caption','wurdig-caption')
                meta.Session.add(post)
                meta.Session.commit()
            except Exception, e:
                pass
        
        response.content_type = 'text/plain'
        return 'done'