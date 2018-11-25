from flask import Flask
from mongoengine import connect
import pymongo
from flask_bootstrap import Bootstrap
from App_Main.Backend.initDB.init_words import init_DB_with_words
from App_Main.Backend.initDB.init_error import init_errordb
from App_Main.Backend.initDB.init_wr import init_urdb
from App_Main.Backend.Config.Config import GlobalConf
from flask_login import LoginManager
from flask_mail import Mail
from flask_register import RegisterManager
import os

Configuration = GlobalConf.getInstance()

APP_MAIN = Flask(__name__,static_folder=Configuration.static_folder,
                 template_folder=Configuration.template_folder)
APP_MAIN.config.from_object(Configuration)


APPBS=Bootstrap(APP_MAIN)
client = pymongo.MongoClient("localhost", 27017)
db = client.zSaad_Test
connect('zSaad_Test', host='127.0.0.1', port=27017)
APPLOGIN = LoginManager(APP_MAIN)
APPLOGIN.login_view = 'hello_world'
APPLOGIN.session_protection = "Strong"
APPREGISTER = RegisterManager(APP_MAIN)
APPREGISTER.register_view='register'
APP_MAIN.config['MAIL_SERVER'] ='smtp.googlemail.com'
APP_MAIN.config['MAIL_PORT'] =587
APP_MAIN.config['MAIL_USE_TLS'] =True
APP_MAIN.config['MAIL_USERNAME'] =os.environ.get('DBUSER') or 'grewebapp@gmail.com'
APP_MAIN.config['MAIL_PASSWORD'] =os.environ.get('DBPASS') or 'Grewebapp22'
mail = Mail(APP_MAIN)


init_DB_with_words()
init_errordb()
init_urdb()


from zKM_Test.Backend.app import routes_KM,model,errors
from zMA_Test.Backend.app import routes_amit,routes_mou,model
from App_Main.Backend.App import routes_saad,model
from App_Main.Backend.initDB.init_admin import init_admin_db

init_admin_db()