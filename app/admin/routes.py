from flask import ( flash, render_template, Blueprint, url_for, abort, redirect
)
from flask_login import current_user, login_required
from app.admin.forms import CategoriesForm
from app.models import Categories
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
		category = Categories(category_name=form.name.data)
		try:
			#add the category to the database
			db.session.add(category)
			db.session.commit()
			flash("You have successfully added a new category")

		except Exception as e:
			#incase category name already exists
			flash('Error: category name already exits. ')

			#return to the categories page
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
		category.category_name = form.name.data
		db.session.commit()
		flash("You have successfully edited the category")

		#redirect to the categories page
		return redirect(url_for('admin.list_categories'))
	#form.description.data = category.description
	form.name.data = category.category_name

	return render_template('admin/categories/category.html', action="Edit",
                           add_category=add_category, form=form,
                           category=category, title="Edit Category")




@admin.route('/categories/delete/<int:id>')
def delete_category(id):
	category = Categories.query.get_or_404(id)
	db.session.delete(category)
	db.session.commit()
	flash("You have successfully deleted a Category")

	#redirect to Cateogries page
	return redirect(url_for('admin.list_categories'))

	return render_template(title = "Delete Category")