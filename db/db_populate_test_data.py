'''
@author: Keng Siang Lee
@since: 28 Jun 2015
Simple python script to populate existing sqlite db with some test data.
Existing data will be removed when creating these data.
'''

from datetime import datetime

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

# helper functions to populate the db
def addUser(email, name, picture):
	'''add a category to the db'''
	user = User(email=email, name=name, picture=picture)
	session.add(user)
	session.commit()
	print 'added user: %s' % user.email
	return user

def addCategory(name, creator_email):
	'''add a category to the db'''
	category = Category(name=name, creator_email=creator_email)
	session.add(category)
	session.commit()
	print 'added category: %s' % category.name
	return category

def addItem(name, description, category, creator_email):
	'''add an item to the db'''
	item = Item(name=name, description=description, category=category, creation_time=datetime.utcnow(), creator_email=creator_email)
	session.add(item)
	session.commit()
	print 'added item: %s' % item.name
	return item

print

# delete all data in the db first
session.query(User).delete()
session.query(Category).delete()
session.query(Item).delete()
print 'deleted all data in db'
print

# add test user
user1 = addUser('test@test.com', 'The One', 'test.png')
print

# add test categories
baseball = addCategory('Baseball', 'test@test.com')
hockey = addCategory('Hockey', 'test@test.com')
snowboarding = addCategory('Snowboarding', 'test@test.com')
soccer = addCategory('Soccer', 'test@test.com')
print

# add test items
addItem('Bat', 'Really cool baseball bat', baseball, 'test@test.com')
addItem('Goggles', 'Protect your eyes with these goggles', snowboarding, 'test@test.com')
addItem('Snowboard', 'Cool snowboard', snowboarding, 'test@test.com')
addItem('Shinguards', 'Protect your shins with these guards', soccer, 'test@test.com')
addItem('Jersey', 'Look like a pro with this jersey', soccer, 'test@test.com')
print

# display current state of the db as a sanity check
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