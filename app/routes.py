from app import app
from flask import (render_template, request, redirect, url_for, session,
	flash
	)

from app.models import db,Admin
import gc
from app.forms import AdminRegForm, LoginForm
from flask_login import (current_user, login_user, logout_user, login_required
	)



@app.route('/logout/')
@login_required
def logout():
    logout_user()
    gc.collect()
    return redirect(url_for('home'))

@app.route('/')
def home():
	
	return render_template("index.html")



@app.route('/admin/')
def admin():
	flash("admin dashboard")
	return render_template('admin_dashboard.html')


@app.route('/admin/register/', methods = ["GET","POST"])
def admin_register():
	form = AdminRegForm(request.form)
	try:
		error = ' '
		if form.validate_on_submit():
			admin = Admin(firstname = form.firstname.data, lastname = form.lastname.data,
				phonenumber=form.phonenumber.data)
			admin.set_password(form.password.data)
			db.session.add(admin)
			db.session.commit()
			gc.collect()
			flash("Congratulations, Registration was successful")
			return redirect(url_for('admin_login'))
		return render_template('register.html', form = form)

	except Exception as e:
		return render_template('register.html', form = form, error= error)


@app.route('/admin/login/', methods=["GET", "POST"])
def admin_login():
	form = LoginForm()
	error = ' '
	try:
		if current_user.is_authenticated:
			flash("you are already logged in")
			return redirect(url_for('admin'))
		if form.validate_on_submit():
			admin = Admin.query.filter_by(email=form.email.data).first()
			if admin is None or not admin.check_password(form.password.data):
				flash("invalid username or password")
				return redirect(url_for('admin_login', form = form))
			login_user(admin)
			gc.collect()
			flash("you have been successfully logged in")
			return redirect(url_for('admin'))
		return render_template('login.html', form = form)
	except Exception as e:
		return render_template('login.html', form= form, error= error)
