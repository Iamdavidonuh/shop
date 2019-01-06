from app import app
from flask import (render_template, request, redirect, url_for, session,
	flash, Blueprint
	)

from app.models import User, ShippingInfo
import gc

from flask_login import (current_user, login_user, logout_user, login_required
	)
from app.users.forms import ShippingForm,ResetPassword
from app import db

users = Blueprint('users', __name__)

@users.route('/cart/')
def cart():	
	return render_template('users/cart.html')


@users.route('/profile/')
def profile():
	form = ShippingForm()
	shipping = ShippingInfo.query.all()
	if form.validate_on_submit():
		info = ShippingInfo(address1=form.address1.data,address2=form.address2.data,
		postcode=form.postcode.data,city=form.city.data,
		state=form.state.data,country=form.country.data)
		db.session.add(info)
		db.session.commit()
		flash('shipping information was submitted successfully')
		return redirect(url_for('users.profile'))
	return render_template('users/profile.html', title = "Account page",form=form,
	shipping = shipping)

@users.route('/profile/change-password/')
def change_password():
	form = ResetPassword()
	return render_template('users/change-password.html',title = 'change password',
	form = form)