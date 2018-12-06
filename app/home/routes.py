from app import app
from flask import (render_template, request, redirect, url_for, session,
	flash,Blueprint
	)

home = Blueprint('home', __name__)



@home.route('/')
def homepage():	
	return render_template("index.html", )


