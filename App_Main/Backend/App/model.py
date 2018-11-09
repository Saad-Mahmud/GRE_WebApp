from mongoengine import *


class Uniquekey(Document):
    g = StringField(required=True,max_length=1)
