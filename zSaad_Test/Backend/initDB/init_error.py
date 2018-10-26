import random
from zSaad_Test.Backend.app.model import Suggestions
import datetime

TYPEr =['Translation','Meaning','Usage','Error','New Words','Bug']
statusr = ['US','TD']
report = 'This is a generic suggestion for testing.This is a generic suggestion for testing.' + 'This is a generic suggestion for testing.This is a generic suggestion for testing.'


def init_errordb():
    Suggestions.objects.delete()
    for i in range(100):
        tp = TYPEr[random.randint(0,5)]
        st = statusr[random.randint(0,1)]
        dt = str(datetime.datetime.now())
        Suggestions(TYPE=tp,report=report,status=st,date=dt).save()