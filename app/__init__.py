from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_uploads import configure_uploads,UploadSet,IMAGES
from flask_mail import Mail


stripe_keys = {
    'secret_key': 'sk_test_oeTw14HnAuwKNWSSpRA5jRNh00jrCoutpu',
    'publishable_key':'pk_test_PMYmr7zLHh7PM61spR2m1hBY001qeaCAFs'
		}

app = Flask(__name__)
app.config.from_object(Config)


'''
creating an object instantiated by uploadedset
which takes 'photos' as name of the file and IMAGES as the type of 
file we wanna accept
'''
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


db = SQLAlchemy(app)

#db.create_all
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

Bootstrap(app)
mail = Mail(app)

from app import models

from app.admin.routes import admin 
from app.auth.routes import auth 
from app.home.routes import home 
from app.users.routes import users 

app.register_blueprint(admin, url_prefix = '/admin')
app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(users)