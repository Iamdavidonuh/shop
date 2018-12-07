from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#db.create_all
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'

Bootstrap(app)


from app import models

from app.admin.routes import admin 
from app.auth.routes import auth 
from app.home.routes import home 
from app.users.routes import users 

app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(users)