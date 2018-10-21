from mongoengine import *
import pymongo
'''
client = pymongo.MongoClient("localhost", 27017)
db = client.zMou_Test #DBname
connect('zMou_Test', host='127.0.0.1', port=27017)

def init_DB_with_words():
    wordID = "A_[aberrant]_MAIN"
    word = "aberrant"
    meanings = [ "markedly different from an accepted norm" ]
    usages = ["When the financial director started screaming and throwing food at his co-workers,"
              +" the police had to come in to deal with his aberrant behavior."]
    TYPE = "adjective"
    ret = Words_Test(wordID=wordID,word=word,meanings=meanings,usages=usages,TYPE=TYPE).save()
    return




class Words_Test(Document):
    wordID = StringField(required=True,max_length=50,primary_key=True)
    word = StringField(required=True,max_length=50,unique=True)
    meanings = ListField(required=True)
    usages = ListField()
    TYPE= StringField(required=True)

init_DB_with_words()

'''


