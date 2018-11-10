import random
from App_Main.Backend.Suggestions.Mediator import suggestions, TODO
import datetime
from App_Main.Backend.Config.DBConfig import DBConf


def init_errordb():
    suggestions.objects.delete()
    TODO.objects.delete()
    Conf = DBConf.getInstance()
    for i in range(10):
        tp = Conf.TYPEr[random.randint(0,5)]
        st = Conf.statusr[random.randint(0,1)]
        dt = str(datetime.datetime.now())
        if(st=='US'):
            suggestions(username ='dummy'+str(i), TYPE=tp, report=Conf.report, status=st, date=dt).save()
        else:
            TODO(username ='dummy'+str(i), TYPE=tp,report=Conf.report,status=st,date=dt).save()
