import os
from flask import ( flash, render_template, Blueprint, url_for, abort, redirect,
request
)
from flask_login import current_user, login_required
from app.admin.forms import CategoriesForm, ProductsForm
from app.models import Categories, Products,Order
from app import photos
from config import Config
import gc
from app import db

admin = Blueprint('admin', __name__)



def check_admin():
	if not current_user.is_admin:
		abort(403)


@admin.route('/categories', methods = ['GET','POST'])
@login_required
def list_categories():
	'''
	Get all product categories
	first check if user is an admin
	'''


	check_admin()

	categories = Categories.query.all()

	return render_template('admin/categories/categories.html', title = "Product Categories",
		categories = categories)


@admin.route('/categories/add/', methods = ['GET','POST'])	
def add_category():
	"""
	add a category to the
	database
	"""
	check_admin()

	add_category = True

	form = CategoriesForm()
	
	if form.validate_on_submit():
		filename = request.files['image']
		_, f_ext = os.path.splitext(filename.filename)
		name = form.name.data
		picture_fn = name + f_ext
		photos.save(filename, name = picture_fn)
		url = photos.url(picture_fn)
		category = Categories(category_name=form.name.data, category_image = url)
		try:
			db.session.add(category)
			db.session.commit()
			flash("You have successfully added a new category")
			gc.collect()
		except Exception as e:
			flash('Error: category name already exits. ')
			
		return redirect(url_for('admin.list_categories'))
	return render_template('admin/categories/category.html', action = "Add", form = form,
		add_category = add_category, title = "Add Categories")



@admin.route('/categories/edit/<int:id>', methods = ["GET","POST"])
def edit_category(id):
	'''
		Edit a category name
	'''

	check_admin()

	add_category = False

	category = Categories.query.get_or_404(id)

	form =CategoriesForm(obj=category)
	if form.validate_on_submit():
		filename = request.files['image']
		_, f_ext = os.path.splitext(filename.filename)
		name = form.name.data
		picture_fn = name + f_ext
		#get the name of the previous image
		previous_img_name = picture_fn
		photos.save(filename, name = picture_fn)
		url = photos.url(picture_fn)

		category.category_name = form.name.data
		category.category_image = url
		db.session.commit()
		gc.collect()
		flash("You have successfully edited the category")

		#remove the changed picture from the folder
		img_dir = Config.UPLOADED_PHOTOS_DEST+'/'
		os.remove(img_dir+previous_img_name)

		#redirect to the categories page
		return redirect(url_for('admin.list_categories'))
	#form.description.data = category.description
	form.name.data = category.category_name

	return render_template('admin/categories/category.html', action="Edit",
                           add_category=add_category, form=form,
                           category=category, title="Edit Category")




@admin.route('/categories/delete/<int:id>', methods = ["GET","POST"])
def delete_category(id):
	category = Categories.query.get_or_404(id)
	
	#get image extension
	_, f_ext = os.path.splitext(category.category_image)
	
	previous_img_name = category.category_name + f_ext
	img_dir = Config.UPLOADED_PHOTOS_DEST+'/'
	os.remove(img_dir+previous_img_name)
	db.session.delete(category)
	db.session.commit()
	gc.collect()
	flash("You have successfully deleted a Category")

	return redirect(url_for('admin.list_categories'))
'''
	return render_template('admin/categories/category.html',
	title = "Delete Category")
'''
@admin.route('/products/')
@login_required
def list_products():
	check_admin()
	'''
	list all products
	'''
	products = Products.query.all()

	return render_template('admin/products/products.html', title = 'Products', products = products)



@admin.route('/products/add/', methods = ["GET","POST"])
@login_required
def add_product():
	'''
	add a product to the database
	'''

	add_product = True

	form = ProductsForm()
	if form.validate_on_submit():
		filename = request.files['image']
		_, f_ext = os.path.splitext(filename.filename)
		name = form.name.data
		picture_fn = name + f_ext
		photos.save(filename, name = picture_fn)
		url = photos.url(picture_fn)
		product = Products(product_name = form.name.data,
		product_price = form.price.data,product_image = url,
		product_description = form.description.data, product_stock = form.stock.data )
		product.products_categories = form.categories.data
		try:
			#add a product to the database
			db.session.add(product)
			db.session.commit()
			gc.collect()
			flash("You have successfully added a product")
		except:
			# in case product name already exists
			flash("Error: product name already exits")
		
		# redirect to the roles page
		return redirect(url_for('admin.list_products'))
	#load product template
	return render_template('admin/products/product.html', add_product = add_product,
	form = form, title = "Add Product")



@admin.route('/products/edit/<int:id>',  methods = ["GET","POST"])
@login_required
def edit_product(id):
	'''
	edit product
	'''
	check_admin()


	add_product = False

	product = Products.query.get_or_404(id)
	form = ProductsForm(obj=product)
	if form.validate_on_submit():
		filename = request.files['image']
		_, f_ext = os.path.splitext(filename.filename)
		
		name = form.name.data
		picture_fn = name + f_ext
		
		#get the name of the previous image
		previous_img_name = picture_fn

		photos.save(filename, name = picture_fn)
		url = photos.url(picture_fn)

		product.product_name = form.name.data
		product.product_price = form.price.data
		product.product_image = url 
		product.product_description = form.description.data
		product.product_stock = form.stock.data
		db.session.commit()
		gc.collect()

		#remove the changed picture from the folder
		img_dir = Config.UPLOADED_PHOTOS_DEST+'/'
		os.remove(img_dir+previous_img_name)
		
		flash('You have successfully edited a product')
		#redirect to the products page
		redirect(url_for('admin.list_products'))

		form.name.data = product.product_name
		form.price.data = product.product_price
		form.image.data = product.product_image  
		form.description.data = product.product_description
		form.stock.data = product.product_stock 

	return render_template('admin/products/product.html', add_product = add_product,
		form = form, title = "Edit Product")


@admin.route('/products/delete/<int:id>', methods = ["GET","POST"])
@login_required
def delete_product(id):
	'''
	Delete a product from the database
	'''
	check_admin()
	
	product = Products.query.get_or_404(id)
	
	#get image extension
	_, f_ext = os.path.splitext(product.product_image)
	
	previous_img_name = product.product_name+f_ext
	img_dir = Config.UPLOADED_PHOTOS_DEST+'/'
	#remove the changed picture from the folder
	os.remove(img_dir+previous_img_name)		
	
	db.session.delete(product)
	db.session.commit()
	gc.collect()
	flash("You have successfully deleted a product")
	
	return redirect(url_for('admin.list_products'))
	

	
@admin.route('/orders/')
@login_required
def list_orders():
	check_admin()
	'''
	list all orders
	'''
	orders = Order.query.all()

	return render_template('admin/orders.html', title = 'Orders', orders = orders)
	