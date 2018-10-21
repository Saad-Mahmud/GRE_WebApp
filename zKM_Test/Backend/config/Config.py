import os

class Config(object):
    GOOGLE_CLIENT_ID = '375961356325-p3umdlkkjr6ak9kairqv8b3ttalio52a.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '8UggTqBUxM3M-9cd8KtLv8Tj'
    REDIRECT_URI = '/oauth2callback'

    SECRET_KEY = os.environ.get('SECRET_KEY') or "You-Will-Never-Guess"
    MONGO_DBNAME = 'restdb'
    MONGO_URI = 'mongodb://localhost:27017/restdb'
