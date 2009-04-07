import logging
import wurdig.model as model
import wurdig.model.meta as meta
import wurdig.lib.helpers as h
import webhelpers.paginate as paginate
import datetime as d
import formencode

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

class UniquePageSlug(formencode.FancyValidator): 
    messages = {
        'invalid': 'Slug must be unique'
    }
    def validate_python(self, value, state):
        filter_kw = {str(self.filter_column): value}
        query = meta.Session.query(self.orm_class)
        item = query.filter_by(**filter_kw).first()
        if item:
            raise formencode.Invalid(
                self.message('invalid', state),
                value, state)
        return value


class NewPageForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    title = formencode.validators.String(
        not_empty=True,
        messages={
            'empty':'Enter a page title'
        }
    )
    slug = formencode.All(
        # @todo: How can I prevent this from validating UniquePageSlug on self/edit
        UniquePageSlug(
            orm_class=model.Page, 
            filter_column='slug'
        ),
        formencode.validators.NotEmpty(
            messages={
                'empty':'Enter a page slug.'
            }
        )
    )
    content = formencode.validators.String(
        not_empty=True,
        messages={
            'empty':'Enter some post content.'
        }
    )

class PageController(BaseController):
    # @todo: delete confirmation
    
    def home(self):
        return render('/derived/page/home.html')

    def view(self, slug=None):
        if slug is None:
            abort(404)
        page_q = meta.Session.query(model.Page)
        c.page = page_q.filter_by(slug=slug).first()
        if c.page is None:
            abort(404)
        c.page.content = h.literal(c.page.content)
        return render('/derived/page/view.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    def new(self):
        return render('/derived/page/new.html')
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewPageForm(), form='new')
    def create(self):
        page = model.Page()
        
        for k, v in self.form_result.items():
            setattr(page, k, v)
            
        meta.Session.add(page)
        meta.Session.commit()
        session['flash'] = 'Page successfully added.'
        session.save()

        return redirect_to(controller='page', 
                           action='view', 
                           slug=page.slug)
    
    @h.auth.authorize(h.auth.is_valid_user)
    def edit(self, id=None):
        if id is None:
            abort(404)
        page_q = meta.Session.query(model.Page)
        page = page_q.filter_by(id=id).first()
        if page is None:
            abort(404)
        values = {
            'title':page.title,
            'slug':page.slug,
            'content':page.content
        }
        return htmlfill.render(render('/derived/page/edit.html'), values)
    
    @h.auth.authorize(h.auth.is_valid_user)
    @restrict('POST')
    @validate(schema=NewPageForm(), form='edit')
    def save(self, id=None):
        page_q = meta.Session.query(model.Page)
        page = page_q.filter_by(id=id).first()
        if page is None:
            abort(404)
            
        for k,v in self.form_result.items():
            if getattr(page, k) != v:
                setattr(page, k, v)
            
        meta.Session.commit()
        session['flash'] = 'Page successfully updated.'
        session.save()

        return redirect_to(controller='page', 
                           action='view', 
                           slug=page.slug)
    
    @h.auth.authorize(h.auth.is_valid_user)
    def list(self):
        pages_q = meta.Session.query(model.Page).order_by(model.Page.created_on.desc())
        c.paginator = paginate.Page(
            pages_q,
            page=int(request.params.get('page', 1)),
            items_per_page = 10,
            controller='page',
            action='list',
        )
        return render('/derived/page/list.html')

    @h.auth.authorize(h.auth.is_valid_user)
    def delete(self, id=None):
        # @todo: delete confirmation
        if id is None:
            abort(404)
        page_q = meta.Session.query(model.Page)
        page = page_q.filter_by(id=id).first()
        if page is None:
            abort(404)
        meta.Session.delete(page)
        meta.Session.commit()
        meta.Session.commit()
        session['flash'] = 'Page successfully deleted.'
        session.save()
        return redirect_to(controller='page', action='list')