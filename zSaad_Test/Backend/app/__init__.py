from flask import Flask
from zSaad_Test.Backend.config import Config
from mongoengine import connect
import pymongo
from flask_bootstrap import Bootstrap
import os
from zSaad_Test.Backend.initDB.init_words import init_DB_with_words

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'Frontend')
template_dir = os.path.join(template_dir, 'templates')
static_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
static_dir = os.path.join(static_dir, 'Frontend')
static_dir = os.path.join(static_dir, 'static')
print(template_dir)

APP_MAIN = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
APP_MAIN.config.from_object(Config.Config)

APPBS=Bootstrap(APP_MAIN)
client = pymongo.MongoClient("localhost", 27017)
db = client.zSaad_Test
connect('zSaad_Test', host='127.0.0.1', port=27017)
init_DB_with_words()

from zSaad_Test.Backend.app import routes,model
