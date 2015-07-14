'''
@author: Keng Siang Lee
@since: 28 Jun 2015
Python script to create schema of the CategoryItems db using SQLAlchemy
'''

# SQLAlchemy modules/functions
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# create base instance
Base = declarative_base()

# create classes for the schema
class User(Base):

	__tablename__ = 'user'

	email = Column(String(250), primary_key=True)
	name = Column(String(250), nullable=False)
	picture = Column(String(250))

class Category(Base):

	__tablename__ = 'category'

	name = Column(String(100), primary_key=True)
	creator_email = Column(String(250), ForeignKey('user.email'))
	user = relationship(User)

class Item(Base):

	__tablename__ = 'item'

	name = Column(String(100), primary_key=True)
	description = Column(String(1000))
	category_name = Column(String(100), ForeignKey('category.name'), primary_key=True)
	category = relationship(Category)
	creation_time = Column(DateTime, nullable=False)
	creator_email = Column(String(250), ForeignKey('user.email'))
	user = relationship(User)

if __name__ == '__main__':
	# create db
	from sqlalchemy import create_engine
	engine = create_engine('sqlite:///categoryitems.db')
	Base.metadata.create_all(engine)