import random
from zSaad_Test.Backend.app.model import Suggestions
import datetime
from App_Main.Backend.Config.DBConfig import DBConf


def init_errordb():
    Suggestions.objects.delete()
    Conf = DBConf.getInstance()
    for i in range(100):
        tp = Conf.TYPEr[random.randint(0,5)]
        st = Conf.statusr[random.randint(0,1)]
        dt = str(datetime.datetime.now())
        Suggestions(TYPE=tp,report=Conf.report,status=st,date=dt).save()