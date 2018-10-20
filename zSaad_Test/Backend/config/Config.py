import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_DBNAME = 'zSaad_Test'
    MONGO_URI = 'mongodb://localhost:27017/zSaad_Test'
