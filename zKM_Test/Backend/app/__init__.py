from flask import Flask
from zKM_Test.Backend.config import Config
from mongoengine import connect
import pymongo
from flask_login import LoginManager
from flask_register import RegisterManager
from flask_bootstrap import Bootstrap
import os
from zKM_Test.Backend.config import Config
from flask_mail import Mail

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir1 = os.path.join(template_dir, 'Frontend')

template_dir = os.path.join(template_dir1, 'templates')
template_dir1 = os.path.join(template_dir1,'static')
print(template_dir1)

APP_MAIN = Flask(__name__,template_folder=template_dir, static_folder=template_dir1)
APP_MAIN.config.from_object(Config.Config)

APPBS=Bootstrap(APP_MAIN)
client = pymongo.MongoClient("localhost", 27017)
db = client.tutorial_mega
connect('tutorial_mega', host='127.0.0.1', port=27017)
APPLOGIN = LoginManager(APP_MAIN)
APPLOGIN.login_view = 'login'
APPLOGIN.session_protection = "Strong"
APPREGISTER = RegisterManager(APP_MAIN)
APPREGISTER.register_view='register'
APP_MAIN.config['MAIL_SERVER'] ='smtp.googlemail.com'
APP_MAIN.config['MAIL_PORT'] =587
APP_MAIN.config['MAIL_USE_TLS'] =True
APP_MAIN.config['MAIL_USERNAME'] =os.environ.get('DBUSER') or 'grewebapp@gmail.com'
APP_MAIN.config['MAIL_PASSWORD'] =os.environ.get('DBPASS') or 'Grewebapp22'
mail = Mail(APP_MAIN)


from zKM_Test.Backend.app import routes,model,errors
