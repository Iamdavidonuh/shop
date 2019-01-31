from app import app, db
from flask import ( render_template, request, redirect, url_for, session,
	flash,Blueprint, abort
	)

from flask_login import current_user, login_required

from app.models import User, Categories, Products,Kart, ProductVariations
from app.admin.forms import Variations

home = Blueprint('home', __name__)


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
	count = Kart.query.filter_by(product_id =Kart.product_id).count()
	return render_template("home/index.html", title = 'Website name',
	categories = categories, products = products, count=count)

@home.route('/<int:id>/')
def shop_by_category(id):

	category = Categories.query.get_or_404(id)
	product = Products.query.get(id)

	count = Kart.query.filter_by(product_id =Kart.product_id).count()
	return render_template("home/shop_by_category.html", category = category,
	product = product, title = "Category: "+ category.category_name,count=count)


@home.route('/productdetails/<int:id>/', methods = ["GET","POST"])
def product_details(id):
	form = Variations() 
	product_detail = Products.query.get_or_404(id)
	user = User.query.get(id)	
	''' 
	try pushing the forms to the admin blueprint and try and if error is 
	same use the populate_obj() func
	'''
	count = Kart.query.filter_by(product_id =Kart.product_id).count()
	if form.validate_on_submit():
		variants = ProductVariations(product_size = form.sizes.data,product_id=product_detail.id)
		cart = Kart(user_id=user.id, product_id=product_detail.id, quantity=1)
		db.session.add(variants)
		db.session.add(cart)
		db.session.commit()
		flash("{} has been added to cart".format(product_detail.product_name))
		
		return redirect(url_for('home.product_details',id = product_detail.id ))
	return render_template("home/productdetails.html",
		product_detail = product_detail,title = product_detail.product_name,
		form =form,count=count)


