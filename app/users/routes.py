from app import app
from flask import (render_template, request, redirect, url_for, session,
	flash, Blueprint
	)

from app.models import db,User
import gc

from flask_login import (current_user, login_user, logout_user, login_required
	)

users = Blueprint('users', __name__)
