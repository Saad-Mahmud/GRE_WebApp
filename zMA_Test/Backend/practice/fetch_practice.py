from mongoengine import *
import pymongo
from zSaad_Test.Backend.initDB.words import Words_Rating


client = pymongo.MongoClient("localhost", 27017)
db = client.zSaad_Test #DBname
connect('zSaad_Test', host='127.0.0.1', port=27017)


def fetch_easy():
    print("I came in fetch_easy", Words_Rating.objects.__sizeof__())
    a = Words_Rating.objects
    for _ in a:
        print("hiiiiiiiiiiiiiiiiiiii")
        print(_.wordID)
    return


