from mongoengine import *


class session_practice(Document):
    #sessionID = StringField(required=True,max_length=50)
    words = ListField(required=True)
    idx = IntField()
    status = DictField()

class session_test(Document):
    words = ListField(required=True)
    idx = IntField()
    status = DictField()