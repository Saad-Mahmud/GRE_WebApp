from flask import Flask
from zMA_Test.Backend.config import Config
from mongoengine import connect
import pymongo
from flask_bootstrap import Bootstrap
import os

template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
template_dir = os.path.join(template_dir, 'Frontend')
template_dir = os.path.join(template_dir, 'templates')
print(template_dir)

APP_MAIN = Flask(__name__, template_folder=template_dir)
APP_MAIN.config.from_object(Config.Config)

APPBS=Bootstrap(APP_MAIN)
client = pymongo.MongoClient("localhost", 27017)
db = client.tutorial_mega
connect('zSaad_Test', host='127.0.0.1', port=27017)


from zMA_Test.Backend.app import routes, model
