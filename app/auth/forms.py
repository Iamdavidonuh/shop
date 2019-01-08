
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

from wtforms.validators import ValidationError, DataRequired, Email

from app.models import User


class RegistrationForm(FlaskForm):

	firstname = StringField('First Name', [validators.Length(min=4,max=20)])
	lastname = StringField('Last Name', [validators.Length(min=4,max=20)])
	email = StringField('Email Address', [validators.Length(min=10,max=50,
		message = "Email address must be 10 to 50 characters Long"), validators.Email()]
	)

	phonenumber = StringField('Phone Number', [validators.Length(min=7,max=12), validators.Required()])

	password = PasswordField('Password', [validators.Length(min=8, max=25,
		message="Password must be 8 to 25 characters long"), validators.Required()]
	)
	
	confirm = PasswordField('Repeat Password', [validators.EqualTo('password',
	 	message = "Passwords must match. ")]
	 )
	
	submit = SubmitField('Register')


	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError("Email already in use. ")

	def validate_phone(self, phonenumber):
		user = User.query.filter_by(phonenumber=phonenumber.data).first()
		if user is not None:
			raise ValidationError("phone number  already in use. ")

#general login form
class LoginForm(FlaskForm):
	email = StringField('Email Address', validators=[DataRequired(), Email()])
	password = PasswordField('Password', [validators.DataRequired()])
	submit = SubmitField('Sign In')
