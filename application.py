import os
from datetime import datetime

# Flask modules/functions
from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, flash
app = Flask(__name__)

# SQLAlchemy modules/functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from db.db_setup import Base, Category, Item

# create engine to existing db and bind to it
engine = create_engine('sqlite:///db/categoryitems.db')
Base.metadata.bind = engine

# create a DBSession instance for committing changes to db
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def showAllCategories():
	categories = session.query(Category).all()
	latestItems = session.query(Item).order_by(Item.creation_time.desc()).limit(3)
	return render_template('showAllCategories.html', categories=categories, latestItems=latestItems)

@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItemsInCategory(category_name):
	try:
		items = session.query(Item).filter_by(category_name=category_name)
		categories = session.query(Category).all()
		return render_template('showItemsInCategory.html', category_name=category_name, items=items, categories=categories)
	except NoResultFound:
		abort(404)

@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItem(category_name, item_name):
	try:
		item = session.query(Item).filter_by(name=item_name, category_name=category_name).one()
		return render_template('showItem.html', category_name=category_name, item=item)
	except NoResultFound:
		abort(404)

@app.route('/catalog/items/new/', methods=['GET', 'POST'])
def createItem():
	if request.method == 'POST':

		# read form data first
		# TODO: validate form inputs
		formCategory = request.form['category']
		if formCategory == 'NEW CATEGORY':
			formCategory = request.form['newCategory']
		formCategory = formCategory.title()
		formName = request.form['name'].title()
		formDescription = request.form['description'].capitalize()

		# add category if does not exist
		try:
			category = session.query(Category).filter_by(name=formCategory).one()
		except NoResultFound:
			category = Category(name=formCategory)
			session.add(category)
			session.commit()

		#add item
		try:
			newItem = Item(name=formName, description=formDescription, category_name=category.name, creation_time=datetime.utcnow())
			session.add(newItem)
			session.commit()

			#flash message
			flash('new item created: %s' % newItem.name)
		except IntegrityError:
			session.rollback()
			flash('item %s already exists in category %s' % (formName, formCategory))
			return redirect(url_for('showAllCategories'))


		# redirect to the category page so that we can see this item
		return redirect(url_for('showItemsInCategory', category_name=category.name))
	else:
		# show the create items page for a GET request
		categories = session.query(Category).all()
		return render_template('createItem.html', categories=categories)

@app.route('/catalog/<string:category_name>/<string:item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
	if request.method == 'POST':

		# read form data first
		# TODO: validate form inputs
		formCategory = request.form['category']
		if formCategory == 'NEW CATEGORY':
			formCategory = request.form['newCategory']
		formCategory = formCategory.title()
		formName = request.form['name'].title()
		formDescription = request.form['description'].capitalize()

		# add category if does not exist
		try:
			category = session.query(Category).filter_by(name=formCategory).one()
		except NoResultFound:
			category = Category(name=formCategory)
			session.add(category)
			session.commit()

		# find the instance
		try:
			item = session.query(Item).filter_by(name=item_name, category_name=category_name).one()
		except NoResultFound:
			abort(404)

		# update the instance
		item.name = formName
		item.description = formDescription
		item.category_name = category.name
		session.add(item)
		session.commit()

		#flash message
		flash('item edited: %s' % item.name)

		# redirect to show item page to see the updated info
		return redirect(url_for('showItemsInCategory', category_name=category.name))
	else:
		try:
			# get the item to edit
			item = session.query(Item).filter_by(name=item_name, category_name=category_name).one()

			# show the edit item page for a GET request
			categories = session.query(Category).all()
			return render_template('editItem.html', categories=categories, category_name=category_name, item=item)
		except NoResultFound:
			abort(404)

@app.route('/catalog/<string:category_name>/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
	if request.method == 'POST':
		try:
			item = session.query(Item).filter_by(name=item_name, category_name=category_name).one()
			session.delete(item)
			session.commit()

			#flash message
			flash('item deleted: %s' % item_name)

			return redirect(url_for('showItemsInCategory', category_name=category_name))
		except NoResultFound:
			abort(404)
	else:
		try:
			item = session.query(Item).filter_by(name=item_name, category_name=category_name).one()
			return render_template('deleteItem.html', category_name=category_name, item=item)
		except NoResultFound:
			abort(404)

@app.route('/catalog.json')
def getCatalogJson():
	result = {}
	categories = session.query(Category).all()
	for category in categories:
		result[category.name] = []
		items = session.query(Item).filter_by(category_name=category.name)
		for item in items:
			result[category.name].append({
				'name': item.name,
				'description': item.description,
				'creation_time': item.creation_time
			})
	return jsonify(result)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.secret_key = os.urandom(123)
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)