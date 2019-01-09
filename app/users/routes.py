from app import app
from flask import (render_template, request, redirect, url_for, session,
	flash, Blueprint
	)

from app.models import User, ShippingInfo, Kart

import gc

from flask_login import (current_user, login_user, logout_user, login_required
	)
from app.users.forms import ShippingForm,RequestResetForm,ResetPasswordForm
from app import db, mail
from flask_mail import Message

users = Blueprint('users', __name__)

@users.route('/cart/')
def cart():	
	counter = Kart.query.filter_by(product_id =Kart.product_id).count()
	# fetch cart data 
	cartlist = Kart.query.filter_by(user_id=Kart.user_id)
	return render_template('users/cart.html', counter = counter, cartlist= cartlist,
	title = "Cart")


@users.route('/profile/')
def profile():
	counter = Kart.query.filter_by(product_id =Kart.product_id).count()

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
	shipping = shipping, counter=counter)


def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com',
	recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{ url_for('users.reset_token', token = token, _external =True) }
If you did not make this request simply ignore this request and no changes will be made.
'''
	mail.send(msg)


@users.route('/profile/reset_password/',methods = ["GET","POST"])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('home.homepage'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset you password','info')
		return redirect(url_for('auth.login'))
	return render_template('users/reset_request.html',title = 'Reset password',
	form = form)




@users.route('/profile/reset_password/<token>/',methods = ["GET","POST"])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('home.homepage'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		user.password_hash = user.set_password(form.password.data)
		db.session.commit()
		flash('Your password has been successfully updated', 'success')
		return redirect(url_for('auth.login'))
	return render_template('users/change-password.html',title = 'Reset password',
	form = form)
