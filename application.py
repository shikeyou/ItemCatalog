# =================================
# IMPORTS
# =================================

import os
from datetime import datetime
import random
import string
import json

# Flask modules/functions
from flask import Flask, render_template, abort, request, redirect, url_for, jsonify, flash, make_response
from flask import session as login_session
app = Flask(__name__)

# Authentication modules/functions
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

# Web modules/functions
import httplib2
import requests

# SQLAlchemy modules/functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from db.db_setup import Base, Category, Item

# =================================
# INIT
# =================================

# create engine to existing db and bind to it
engine = create_engine('sqlite:///db/categoryitems.db')
Base.metadata.bind = engine

# create a DBSession instance for committing changes to db
DBSession = sessionmaker(bind=engine)
session = DBSession()

# get client id
with open('client_secrets.json', 'r') as f:
	client_web_data_json = json.loads(f.read())['web']
	CLIENT_ID = client_web_data_json['client_id']

# =================================
# ROUTES
# =================================

@app.route('/')
def showAllCategories():
	categories = session.query(Category).all()
	latestItems = session.query(Item).order_by(Item.creation_time.desc()).limit(3)
	return render_template('showAllCategories.html', categories=categories, latestItems=latestItems, login_session=login_session)

@app.route('/catalog/<string:category_name>/')
@app.route('/catalog/<string:category_name>/items/')
def showItemsInCategory(category_name):
	try:
		items = session.query(Item).filter_by(category_name=category_name)
		categories = session.query(Category).all()
		return render_template('showItemsInCategory.html', category_name=category_name, items=items, categories=categories, login_session=login_session)
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

	# check if user is logged in first
	if 'username' not in login_session:
		return redirect('/login')

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

	# check if user is logged in first
	if 'username' not in login_session:
		return redirect('/login')

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

	# check if user is logged in first
	if 'username' not in login_session:
		return redirect('/login')

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

@app.route('/login/')
def showLogin():

	# create a state token to prevent request forgery
	state = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in xrange(32))
	# store it in the session for later verification
	login_session['state'] = state
	# return 'The current session state is %s' % login_session['state']
	return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():

	# check that the token provided by server to client
	# is the same as the one returned from client to server
	# to prevent cross-site forgery attacks
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# get the one-time-use code sent from client to server
	code = request.data

	# exchange code for credentials with google api server
	try:
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# check that the access token in this credentials is valid
	access_token = credentials.access_token
	url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response

	# verify that access token is for the intended user
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps('User ID in token does not match given user ID'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# verify that access token is actually for our app
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps('Client ID in token does not match client ID of app'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# check if user is already logged in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and stored_gplus_id == gplus_id:
		response = make_response(json.dumps('Current user is already connected'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# by now, we should have a valid access token from google on our server
	# and we can request for any permissible info we need

	# store access token in the session for later use
	login_session['credentials'] = credentials.access_token
	login_session['gplus_id'] = gplus_id

	# get user info and store them in the session
	userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)
	data = answer.json()
	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash('you are now logged in as %s' % login_session['username'])
	print 'done!'
	return output

@app.route('/gdisconnect')
def gdisconnect():

	# check that user must be logged in in the first place
	credentials = login_session.get('credentials')
	if credentials is None:
		response = make_response(json.dumps('Current user is not connected'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# execute GET request to revoke token
	access_token = credentials
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200':  # successful revoke

		# reset user's session
		del login_session['credentials']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']

		# return status code 200
		response = make_response(json.dumps('Successfully disconnected'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	else:

		# return error
		response = make_response(json.dumps('Successfully disconnected'), 400)
		response.headers['Content-Type'] = 'application/json'
		return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
	app.secret_key = os.urandom(123)
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)