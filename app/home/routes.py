from app import app, db
from flask import ( render_template, request, redirect, url_for, session,
	flash,Blueprint, abort
	)

from flask_login import current_user, login_required

from app.models import User, Categories, Products,Kart
from app.admin.forms import Variations
import random
home = Blueprint('home', __name__)


@home.route('/admin/dashboard/')
@login_required
def admin_dashboard():
	#preventing non admins from accessing the page
	if not current_user.is_admin:
		abort(403)
	return render_template('admin/admin_dashboard.html' , title = "Dashboard")

@home.route('/')
def landing():
	ids = []
	c = Products.query.all()
	for s in c:
		ids.append(s.id)
	sorter = []
	for i in range(3):
		random.randint(1,1000)
		if i in ids:
			sorter.append(i)
	products = Products.query.all()
	return render_template('head.html', products = products, sorter = sorter)

@home.route('/home/')
def homepage():		
	categories = Categories.query.all()
	products = Products.query.all()

	if current_user.is_anonymous:
		count = 0
	else:
		count = Kart.query.filter_by(user_id =current_user.id).count()
	return render_template("home/index.html", title = 'Website name',
	categories = categories, products = products, count=count)

@home.route('/<int:id>/')
def shop_by_category(id):
	if current_user.is_anonymous:

		count = 0
	else:
		count = Kart.query.filter_by(user_id =current_user.id).count()

	page = request.args.get('page',1, type=int)
	
	category = Categories.query.get_or_404(id)
	product = Products.query.filter_by(categories_id=category.id)\
		.order_by(Products.product_name).paginate(page=page, per_page=6)
	prod_id = Products.query.get(id)
	return render_template("home/shop_by_category.html", category = category,\
		product = product, title = "Category: "+ category.category_name,count=count,\
		prod_id = prod_id)


@home.route('/productdetails/<int:id>/', methods = ["GET","POST"])
def product_details(id):
	if current_user.is_anonymous:
		count = 0
	else:
		count = Kart.query.filter_by(user_id =current_user.id).count()
		user =current_user.id
	form = Variations()
	product_detail = Products.query.get_or_404(id)
	 
		
	# add to cart
	if form.validate_on_submit():
		# annonymous users
		if current_user.is_anonymous:
			flash('please login before you can add items to your shopping cart','warning')
			return redirect(url_for("home.product_details",id = product_detail.id))
		# authenticated users
		product_detail.product_size = form.sizes.data
		cart = Kart(user_id=user, product_id=product_detail.id, quantity=1,
		subtotal = product_detail.product_price)
		db.session.add(cart)
		db.session.commit()

		flash("{} has been added to cart".format(product_detail.product_name))	
		return redirect(url_for('home.product_details',id = product_detail.id ))
	return render_template("home/productdetails.html",
		product_detail = product_detail,title = product_detail.product_name,
		form =form,count=count)


