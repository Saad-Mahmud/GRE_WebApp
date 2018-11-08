from flask import Flask
from zSaad_Test.Backend.config import Config
from mongoengine import connect
import pymongo
from flask_bootstrap import Bootstrap
from zSaad_Test.Backend.initDB.init_words import init_DB_with_words
from zSaad_Test.Backend.initDB.init_error import init_errordb
from zSaad_Test.Backend.config.Config import GlobalConf

Configuration = GlobalConf.getInstance()

APP_MAIN = Flask(__name__,static_folder=Configuration.static_folder,
                 template_folder=Configuration.template_folder)
APP_MAIN.config.from_object(Configuration)


APPBS=Bootstrap(APP_MAIN)
client = pymongo.MongoClient("localhost", 27017)
db = client.zSaad_Test
connect('zSaad_Test', host='127.0.0.1', port=27017)

init_DB_with_words()
init_errordb()

from zSaad_Test.Backend.app import routes,model
