from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from zDB_Tutorial.Backend.app import APPLOGIN
from hashlib import md5

class User(UserMixin,Document):
    username = StringField(required=True,max_length=50,primary_key=True)
    email = StringField(required=True,max_length=50,unique=True)
    password_hash = StringField(required=True,max_length=128)
    about_me = StringField(max_length=300)
    last_seen = DateTimeField()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

@APPLOGIN.user_loader
def load_user(username):
    return User.objects(username=username)[0]


