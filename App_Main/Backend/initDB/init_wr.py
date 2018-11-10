import random
import datetime
from App_Main.Backend.Config.DBConfig import DBConf
from App_Main.Backend.Words.Words import Words
from zMA_Test.Backend.app.model import user_word_history
color = ['green','yellow','red']

def init_urdb():
    k = Words.objects
    status = {}
    for i in k:
        status[i.wordID]=color[random.randint(0,2)]

    user_word_history(username='asd',status=status).save()
    user_word_history(username='asd1', status=status).save()
    user_word_history(username='asd2', status=status).save()
    user_word_history(username='asd3', status=status).save()
