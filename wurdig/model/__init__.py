"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm, schema, types, func
from sqlalchemy.orm import column_property
from sqlalchemy.sql import and_, select
from wurdig.model import meta

import datetime

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)
    #
    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

def now():
    return datetime.datetime.utcnow()

"""
A key value pair in the settings table can be one of the following types:
t = text
b = boolean
ta = textarea

"""
settings_table = schema.Table('settings', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('setting_seq_id', optional=True), primary_key=True),
    schema.Column('key', types.Unicode(50), nullable=False, unique=True),
    schema.Column('value', types.UnicodeText(), default=u''),
    schema.Column('description', types.Unicode(75), default=u''),
    schema.Column('type', types.Unicode(2), nullable=False, default=u't'),
    schema.Column('help', types.UnicodeText(), default=u''),
)

pages_table = schema.Table('pages', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('page_seq_id', optional=True), primary_key=True),
    schema.Column('title', types.Unicode(100), default=u'Untitled Page'),
    schema.Column('slug', types.Unicode(100), nullable=False, unique=True),
    schema.Column('content', types.UnicodeText(), nullable=False),
    schema.Column('created_on', types.TIMESTAMP(), default=now),
)

posts_table = schema.Table('posts', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('post_seq_id', optional=True), primary_key=True),
    schema.Column('title', types.Unicode(100), default=u'Untitled Post'), 
    schema.Column('slug', types.Unicode(100), nullable=False, unique=True),
    schema.Column('content', types.UnicodeText(), nullable=False),
    schema.Column('comments_allowed', types.Boolean(), default=True),
    schema.Column('created_on', types.TIMESTAMP(), default=now),
    schema.Column('draft', types.Boolean(), default=True),
    schema.Column('posted_on', types.TIMESTAMP(), index=True),
)

comments_table = schema.Table('comments', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('comment_seq_id', optional=True), primary_key=True),
    schema.Column('post_id', types.Integer,
        schema.ForeignKey('posts.id'), nullable=False),
    schema.Column('content', types.UnicodeText(), nullable=False),
    schema.Column('name', types.Unicode(100), nullable=False),
    schema.Column('email', types.Unicode(50), nullable=False),
    schema.Column('url', types.Unicode(125), default=u''),
    schema.Column('created_on', types.TIMESTAMP(), default=now),
    schema.Column('approved', types.Boolean(), default=False),
)

tags_table = schema.Table('tags', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('tag_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(40), nullable=False, unique=True),
    schema.Column('slug', types.Unicode(40), nullable=False, unique=True),
)

poststags_table = schema.Table('posts_tags', meta.metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('posttag_seq_id', optional=True), primary_key=True),
    schema.Column('post_id', types.Integer, schema.ForeignKey('posts.id')),
    schema.Column('tag_id', types.Integer, schema.ForeignKey('tags.id')),
)

class Setting(object):
    pass

class Page(object):
    pass

class Post(object):
    pass

class Comment(object):
    pass

class Tag(object):
    pass

orm.mapper(Setting, settings_table)
orm.mapper(Comment, comments_table)
orm.mapper(Tag, tags_table, order_by='name')

"""
Removing post count for tags.  The operation is expensive
and I just don't care that much
orm.mapper(Tag, tags_table, order_by='name', properties={
    'post_count': column_property(
        select(
            [func.count(posts_table.c.id)],
            and_(
                 poststags_table.c.post_id==posts_table.c.id,
                 poststags_table.c.tag_id==tags_table.c.id
            )
        ).label('post_count')
    )
})
"""

orm.mapper(Page, pages_table, order_by='title')
orm.mapper(Post, posts_table, order_by='posted_on DESC', polymorphic_identity='posts', properties={
    'comments':orm.relation(Comment, backref='posts', cascade='all',order_by='created_on', 
        primaryjoin=and_(
                posts_table.c.id==comments_table.c.post_id, 
                comments_table.c.approved==True
        )
    ),
    'tags':orm.relation(Tag, secondary=poststags_table)
})
