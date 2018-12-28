from app import app
from flask import ( render_template, request, redirect, url_for, session,
	flash,Blueprint, abort
	)

from flask_login import current_user, login_required

from app.models import Categories, Products
from app.home.forms import ProductVariations

home = Blueprint('home', __name__)

@home.route('/test')
def test():	
	return render_template("base.html", title = 'test')



@home.route('/admin/dashboard/')
@login_required
def admin_dashboard():
	#preventing non admins from accessing the page
	if not current_user.is_admin:
		abort(403)
	flash("admin dashboard")
	return render_template('admin/admin_dashboard.html' , title = "Dashboard")


@home.route('/')
def homepage():	
	categories = Categories.query.all()
	products = Products.query.all()
	return render_template("home/index.html", title = 'Website name',
	categories = categories, products = products)

@home.route('/<int:id>/')
def shop_by_category(id):

	category = Categories.query.get_or_404(id)
	product = Products.query.get_or_404(id)

	return render_template("home/shop_by_category.html", category = category,
	product = product, title = "Category: "+ category.category_name)


@home.route('/productdetails/<int:id>/')
def product_details(id):
	
	form = ProductVariations()
	product_detail = Products.query.get_or_404(id)

	return render_template("home/productdetails.html",
	product_detail = product_detail,title = product_detail.product_name,form =form)

@home.route('/add/<int:id>/')
def add_to_cart(id):
	product_detail = Products.query.get_or_404(id)
	'''
	add product to the database 
	with the db bullshit in the appropriate branch
	'''
	flash("{} has been added to cart".format(product_detail.product_name))
	return render_template('home/productdetails.html',
	product_detail = product_detail, title = product_detail.product_name)


@home.route('/productdetails/<int:id>/buy')
def buynow(id):
	product_detail = Products.query.get_or_404(id)

	return render_template('home/buynow.html', product_detail = product_detail,
	title ="Purchase "+ product_detail.product_name )


'''
@home.route('/checkout/<int:id>/')
def checkout(id):
	product_detail = Products.query.get_or_404(id)
	return render_template('home/checkout.html',
	product_detail = product_detail, title = "Purchase "+product_detail.product_name)
'''