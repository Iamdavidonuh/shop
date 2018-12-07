from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired




class CategoriesForm(FlaskForm):
	'''
	Form for admin to add or edit
	a category name
	'''
	name = StringField('Name', [validators.DataRequired()])
	
	submit = SubmitField('Submit')