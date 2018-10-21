from mongoengine import *
from flask_login import UserMixin

from zKM_Test.Backend.app import APPLOGIN
from hashlib import md5
from werkzeug.security import check_password_hash


class User(UserMixin,Document):
    username = StringField(required=True,max_length=50,primary_key=True)
    email = StringField(required=True,max_length=50,unique=True)
    password_hash = StringField(required=True,max_length=128)
    about_me = StringField(max_length=300)
    last_seen = DateTimeField()
    age = StringField()
    country = StringField()
    gender = StringField()
    reg_date = DateTimeField()
    upic = StringField()
    pic = StringField()


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        if self.pic:
            return (self.pic).format(digest, size)
        elif self.upic is None:
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
        digest, size)
        else:
            return self.upic.format(digest,size)


class Country(UserMixin, Document):
    country_id = IntField(required=True, primary_key=True)
    country_name = StringField(required=True, max_length=50, unique=True    )

class Gre_data(UserMixin, Document):
    username =  StringField(required=True, primary_key=True)
    history = ListField(IntField())
    how_many_test = IntField()
    best_score = FloatField()
    avg_score = FloatField()


@APPLOGIN.user_loader
def load_user(username):
    return User.objects(username=username)[0]

