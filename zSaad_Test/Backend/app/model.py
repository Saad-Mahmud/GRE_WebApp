from mongoengine import *

class Suggestions(Document):
    TYPE = StringField(required=True,max_length=50)
    report = StringField(required=True,max_length=500)
    date = StringField(required=True,max_length=50)
    status = StringField(required=True,max_length=5)
