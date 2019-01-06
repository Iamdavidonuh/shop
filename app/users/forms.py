from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, PasswordField, SubmitField, validators

from wtforms.validators import ValidationError, DataRequired

from app.models import User

from flask_login import current_user


class ShippingForm(FlaskForm):
    address1 = StringField('Primary Address',validators=[DataRequired()]) 
    address2 = StringField('Secondary Address', validators=[DataRequired()])
    postcode = IntegerField('Postal code', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('state', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Submit')



class ResetPassword(FlaskForm):
	password = PasswordField('Password', [validators.Length(min=8, max=25,
		message="Password must be 8 to 25 characters long"), validators.Required()]
	)
	
	confirm = PasswordField('Repeat Password', [validators.EqualTo('password',
	 	message = "Passwords must match. ")]
	)
	
	submit = SubmitField('Submit')

	def validate_password(self, password):
		user = User.query.filter_by(current_user.email)
		if User.check_password(user.password_hash,password) is True:
			raise ValidationError("You cannot use a previously selected")

