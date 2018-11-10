
from mongoengine import Document, StringField

class Mediator():


    def swap(self,obj):
        if(obj.status == 'US'):
            print ('US')
            TODO(username=obj.username, TYPE=obj.TYPE,
                        report=obj.report, date=obj.date, id=obj.id, status='TD').save()
            obj.delete()
        else:
            suggestions(username=obj.username, TYPE=obj.TYPE,
                 report=obj.report, date=obj.date, id=obj.id, status='US').save()
            obj.delete()

class TODO(Document):

    username = StringField(required=True, max_length=50)
    TYPE = StringField(required=True, max_length=50)
    report = StringField(required=True, max_length=500)
    date = StringField(required=True, max_length=50)
    status = StringField(required=True, max_length=5)

    def swap(self):
        Mediator().swap(self)


class suggestions(Document):

    username = StringField(required=True,max_length=50)
    TYPE = StringField(required=True,max_length=50)
    report = StringField(required=True,max_length=500)
    date = StringField(required=True,max_length=50)
    status = StringField(required=True,max_length=5)

    def swap(self):
        print ('sg')
        Mediator().swap(self)
