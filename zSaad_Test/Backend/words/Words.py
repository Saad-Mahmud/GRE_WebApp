from mongoengine import *


class Words(Document):
    wordID = StringField(required=True, max_length=50, primary_key=True)
    word = StringField(required=True, max_length=50, unique=True)
    meanings = ListField(required=True)
    usages = ListField()
    translations = DictField()
    TYPE = StringField(required=True)






