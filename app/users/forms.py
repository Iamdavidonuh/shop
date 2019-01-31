from flask_wtf import FlaskForm
from wtforms import(StringField,IntegerField, PasswordField,
SubmitField, validators, SelectField)

from wtforms.validators import ValidationError, DataRequired, Email

from app.models import User

from flask_login import current_user

class CartForm(FlaskForm):
	quantity = IntegerField('1', validators=[DataRequired()])
	submit = SubmitField('Submit')

class ShippingForm(FlaskForm):
    address1 = StringField('Primary Address',validators=[DataRequired()]) 
    address2 = StringField('Secondary Address', validators=[DataRequired()])
    postcode = IntegerField('Postal code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    #country = SelectField('Country', validators=[DataRequired()])
	#country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')




class RequestResetForm(FlaskForm):
	email = StringField('Email Address', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError("There is no account with that email. You must register first")


class ResetPasswordForm(FlaskForm):

	password = PasswordField('Password', [validators.Length(min=8, max=25,
		message="Password must be 8 to 25 characters long"), validators.Required()]
	)
	
	confirm = PasswordField('Repeat Password', [validators.EqualTo('password',
	 	message = "Passwords must match. ")]
	 )
	
	submit = SubmitField('Reset Password')
