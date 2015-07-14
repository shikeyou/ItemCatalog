'''
@author: Keng Siang Lee
@since: 13 Jul 2015
Simple python script to show all data in an existing sqlite db.
'''

# SQLAlchemy modules/functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# our custom db classes
from db_setup import Base, User, Category, Item

# create engine to existing db and bind to it
engine = create_engine('sqlite:///categoryitems.db')
Base.metadata.bind = engine

# create a DBSession instance for committing changes to db
DBSession = sessionmaker(bind = engine)
session = DBSession()

# display current state of the db
print 'Users in db:'
users = session.query(User).all()
for user in users:
	print 'email=%s, name=%s, picture=%s' % (`user.email`, `user.name`, `user.picture`)
print
print 'Categories in db:'
categories = session.query(Category).all()
for category in categories:
	print 'name=%s, creator_email=%s' % (`category.name`, `category.creator_email`)
print
print 'Items in db:'
items = session.query(Item).all()
for item in items:
	print 'name=%s, description=%s, category_name=%s, creation_time=%s, creator_email=%s' % (`item.name`, `item.description`, `item.category.name`, `item.creation_time`, `item.creator_email`)
print