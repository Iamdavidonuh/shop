
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

from wtforms.validators import ValidationError, DataRequired

from app.models import Admin

#admin register form
class AdminRegForm(FlaskForm):

	firstname = StringField('First Name', [validators.Length(min=4,max=20)])
	lastname = StringField('Last Name', [validators.Length(min=4,max=20)])
	email = StringField('Email Address', [validators.Length(min=10,max=50,
		message = "email must be 10 to 50 characters Long")]
	)

	phonenumber = StringField('Number', [validators.Length(min=7,max=12), validators.Required()])

	password = PasswordField('Password', [validators.Required(),validators.Length(min=8, max=25,
		message="password must be 8 to 25 characters long")]
	)
	confirm= PasswordField('Repeat Password', [validators.Required(),validators.EqualTo('password',
		message="password must match")]
	)
	
	submit = SubmitField('Register')


	def validate_email(self, email):
		admin = Admin.query.filter_by(email=email.data).first()
		if admin is not None:
			raise ValidationError("Please use a different email address. ")

#general login form
class LoginForm(FlaskForm):
	email = StringField('Email Address', [validators.DataRequired()])
	password = PasswordField('Password', [validators.DataRequired()])
	submit = SubmitField('Sign In')


