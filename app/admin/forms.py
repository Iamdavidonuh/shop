from flask_wtf import FlaskForm
from wtforms import ( StringField, SubmitField,TextAreaField,IntegerField,
FloatField, validators
)
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField 
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app import photos
from app.models import Categories

class CategoriesForm(FlaskForm):
	'''
	Form for admin to add or edit
	a category name
	'''
	name = StringField('Name', [validators.DataRequired()])
	
	submit = SubmitField('Submit')

class ProductsForm(FlaskForm):
	'''
	Form for admin to add or edit a product
	'''
	categories = QuerySelectField(query_factory=lambda: Categories.query.all(),
	get_label="category_name")
	name = StringField('Product name', [validators.DataRequired()])
	price =IntegerField('Product Price', [validators.DataRequired()])
	image = FileField('product picture', validators=[FileRequired(),
	FileAllowed(photos, "images only")])
	stock = IntegerField('Stock', [validators.DataRequired()])
	description = TextAreaField('describe the product', [validators.DataRequired()])
	submit = SubmitField('Submit')