import logging
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import webhelpers.paginate as paginate
import datetime as d
import formencode
import re

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import restrict
from sqlalchemy.sql import and_, delete
from formencode import htmlfill
from wurdig.lib.base import BaseController, render
from authkit.authorize.pylons_adaptors import authorize

from wurdig.lib.base import BaseController, render

log = logging.getLogger(__name__)

class ConstructSlug(formencode.FancyValidator):
    def _to_python(self, value, state):
        if value['slug'] in ['', u'', None]:
            tag_name = value['name'].lower()
            value['slug'] = re.compile(r'[^\w-]+', re.U).sub('-', tag_name).strip('-')
        return value

class UniqueTagSlug(formencode.FancyValidator):
    messages = {
        'invalid': 'Slug already exists'
    }
    def _to_python(self, value, state):
        query = meta.Session.query(model.Tag)
        if value.has_key('id') and value['id'] is not None:
            # we're editing an existing tag.
            item = query.filter(and_(model.Tag.id!=value['id'], model.Tag.slug==value['slug'])).first()
        else:
            # we're adding a new tag.
            item = query.filter(model.Tag.slug==value['slug']).first()
            
        if item:
            raise formencode.Invalid(
                self.message('invalid', state),
                value, state)
            
        return value

class NewTagForm(formencode.Schema):
    pre_validators = [ConstructSlug()]
    allow_extra_fields = True
    filter_extra_fields = True
    name = formencode.validators.UnicodeString(
        not_empty=True,
        messages={
            'empty':'Enter a tag name'
        },
        strip=True
    )
    slug = formencode.validators.UnicodeString(max=30, strip=True)
    chained_validators = [UniqueTagSlug()]
    
class EditTagForm(NewTagForm):
    id = formencode.validators.Int()

class TagController(BaseController):

    def cloud(self):
        tag_q = meta.Session.query(model.Tag).order_by(model.Tag.name.asc())
        c.tags = tag_q.all()
        if c.tags is None:
            abort(404)
        return render('/derived/tag/cloud.html')
    
    def archive(self, slug=None):   
        if slug is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        c.tag = tag_q.filter(model.Tag.slug==slug).first()
        query = meta.Session.query(model.Post).order_by(model.Post.posted_on.desc())
        c.paginator = paginate.Page(
            query.filter(and_(model.Post.tags.any(slug=slug), model.Post.posted_on != None)).all(),
            page=int(request.params.get('page', 1)),
            items_per_page = 2,
            controller='tag',
            action='archive',
            slug=slug
        )
                
        return render('/derived/tag/archive.html')

    @h.auth.authorize(h.auth.is_valid_user)
    def new(self):
        return render('/derived/tag/new.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewTagForm(), form='new')
    def create(self):
        tag = model.Tag()
        
        for k, v in self.form_result.items():
            setattr(tag, k, v)
            
        meta.Session.add(tag)
        meta.Session.commit()
        session['flash'] = 'Tag successfully added.'
        session.save()
        return redirect_to(controller='tag', action='cloud')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
        values = {
            'id':tag.id,
            'title':tag.name,
            'slug':tag.slug
        }
        return htmlfill.render(render('/derived/tag/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=EditTagForm(), form='edit')
    def save(self, id=None):
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
            
        for k,v in self.form_result.items():
            if getattr(tag, k) != v:
                setattr(tag, k, v)
            
        meta.Session.commit()
        session['flash'] = 'Tag successfully updated.'
        session.save()
        return redirect_to(controller='tag', action='archive', slug=tag.slug)
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        tags_q = meta.Session.query(model.Tag).order_by(model.Tag.name.asc())
        c.paginator = paginate.Page(
            tags_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='tag',
            action='list',
        )
        return render('/derived/tag/list.html')

    @h.auth.authorize(h.auth.is_valid_user)
    def delete(self, id=None):
        # @todo: delete confirmation
        if id is None:
            abort(404)
        tag_q = meta.Session.query(model.Tag)
        tag = tag_q.filter_by(id=id).first()
        if tag is None:
            abort(404)
        meta.Session.execute(delete(model.poststags_table, model.poststags_table.c.tag_id==tag.id))
        meta.Session.delete(post)
        meta.Session.commit()
        session['flash'] = 'Tag successfully deleted.'
        session.save()
        return redirect_to(controller='tag', action='cloud')