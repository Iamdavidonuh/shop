from flask import flash, render_template, Blueprint

admin = Blueprint('admin', __name__)



@admin.route('/dashboard/')
def admin_dashboard():
	flash("admin dashboard")
	return render_template('admin/admin_dashboard.html')

