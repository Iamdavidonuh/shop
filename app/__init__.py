from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'auth.login'



from app import models

from app.admin.routes import admin as admin_blueprint
from app.auth.routes import auth as auth_blueprint
from app.home.routes import home as home_blueprint
from app.users.routes import users as users_blueprint

app.register_blueprint(admin_blueprint, url_prefix = '/admin')
app.register_blueprint(auth_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(users_blueprint)