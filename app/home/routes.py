from app import app
from flask import ( render_template, request, redirect, url_for, session,
	flash,Blueprint, abort
	)

from flask_login import current_user, login_required

home = Blueprint('home', __name__)

@home.route('/admin/dashboard/')
@login_required
def admin_dashboard():
	#preventing non admins from accessing the page
	if not current_user.is_admin:
		abort(403)
	flash("admin dashboard")
	return render_template('admin/admin_dashboard.html' , title = "Dashboard")


@home.route('/')
def homepage():	

	
	return render_template("index.html")


