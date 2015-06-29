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
from db_setup import Base, Category, Item

# create engine to existing db and bind to it
engine = create_engine('sqlite:///db/categoryitems.db')
Base.metadata.bind = engine

# create a DBSession instance for committing changes to db
DBSession = sessionmaker(bind = engine)
session = DBSession()

# helper functions to populate the db
def addCategory(name):
	'''add a category to the db'''
	category = Category(name=name)
	session.add(category)
	session.commit()
	print 'added category: %s' % category.name
	return category

def addItem(name, description, category):
	'''add an item to the db'''
	item = Item(name=name, description=description, category=category, creation_time=datetime.utcnow())
	session.add(item)
	session.commit()
	print 'added item: %s' % item.name
	return item

print

# delete all data in the db first
session.query(Category).delete()
session.query(Item).delete()
print 'deleted all data in db'
print

# add test categories
baseball = addCategory('Baseball')
hockey = addCategory('Hockey')
snowboarding = addCategory('Snowboarding')
soccer = addCategory('Soccer')
print

# add test items
addItem('Bat', 'Really cool baseball bat', baseball)
addItem('Goggles', 'Protect your eyes with these goggles', snowboarding)
addItem('Snowboard', 'Cool snowboard', snowboarding)
addItem('Shinguards', 'Protect your shins with these guards', soccer)
addItem('Jersey', 'Look like a pro with this jersey', soccer)
print

# display current state of the db as a sanity check
print 'Categories in db:'
categories = session.query(Category).all()
for category in categories:
	print 'name=%s' % (`category.name`)
print
print 'Items in db:'
items = session.query(Item).all()
for item in items:
	print 'name=%s, description=%s, category_name=%s, creation_time=%s' % (`item.name`, `item.description`, `item.category.name`, `item.creation_time`)
print