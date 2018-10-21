from mongoengine import *
import pymongo
from zSaad_Test.Backend.initDB.words import Words_Rating



def fetch_easy():
    print("I came in fetch_easy", Words_Rating.objects.__sizeof__())
    a = Words_Rating.objects
    print(a)
    for _ in a:
        print("hiiiiiiiiiiiiiiiiiiii")
        print(_.wordID)
    return


