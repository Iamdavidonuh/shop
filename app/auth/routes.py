from app import app
from flask import (render_template, request, redirect, url_for, session,
	flash, Blueprint
	)

from app.models import db,User
import gc
from app.auth.forms import RegistrationForm, LoginForm
from flask_login import (current_user, login_user, logout_user, login_required
	)

auth = Blueprint('auth', __name__)




@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    gc.collect()
    return redirect(url_for('home.homepage'))


@auth.route('/register/', methods = ["GET","POST"])
def register():
	form = RegistrationForm(request.form)
	try:
		error = ' '
		if form.validate_on_submit():
			user = User(firstname = form.firstname.data, lastname = form.lastname.data,
				phonenumber=form.phonenumber.data,email = form.email.data,)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			gc.collect()
			flash("Congratulations, Registration was successful")
			return redirect(url_for('auth.login'))
		return render_template('register.html', form = form)

	except Exception as e:
		return render_template('register.html', form = form, error= error)


@auth.route('/login/', methods=["GET", "POST"])
def login():
	form = LoginForm()
	error = ' '
	try:
		if current_user.is_authenticated:
			flash("you are already logged in")
			return redirect(url_for('home.homepage'))
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			if user is None or not user.check_password(form.password.data):
				flash("invalid username or password")
				return redirect(url_for('auth.login', form = form))
			login_user(user)

			#check if user is an admin or not and login to the appropriate place
			if user.is_admin:
				return redirect(url_for('admin.admin_dashboard'))
			else:
				return redirect(url_for('home.homepage'))
			gc.collect()
			flash("you have been successfully logged in")
		return render_template('login.html', form = form)
	except Exception as e:
		return render_template('login.html', form= form, error= error)
