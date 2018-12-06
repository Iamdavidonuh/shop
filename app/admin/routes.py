from flask import flash, render_template, Blueprint

admin = Blueprint('admin', __name__)



@admin.route('/admin/')
def admin_dashboard():
	flash("admin dashboard")
	return render_template('admin_dashboard.html')

