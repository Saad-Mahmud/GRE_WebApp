from mongoengine import *
import pymongo
from flask import Flask
import random
from zKM_Test.Backend.app.model import User, Country,Gre_data
from werkzeug.security import generate_password_hash
app = Flask(__name__)

client = pymongo.MongoClient("localhost",27017)
db = client.tutorial_mega
connect('tutorial_mega', host="127.0.0.1", port = 27017)


pword = 'abc'
for i in range(1,11,1):
    user = User(username=str(i),
                email=str(i)+'@gmail.com',
                password_hash=generate_password_hash(pword))
    user.save()
    gre_record = Gre_data(username=str(i))
    gre_record.save()

'''
cntttt = ["Bangladesh","America","England","Syria","Uganda","Honululu","India","Pakistan","Brazil","Argentina"]
for i in range(1,11,1):
    cnt = Country(country_id=i,
                  country_name=cntttt[i-1])
    cnt.save()

collection = db['country']
cursor = collection.find({})
for i in cursor:
    print(i['country_name'])
'''
if __name__== "__main__":
    app.run(debug=True)

'''   //////////////dummy stat creation in routes.py def stat() ///////////
    label = []
    val = []
    col = db['gre_data']
    cursor = col.find({})
    for i in cursor:
        stat_data = Gre_data.objects(username=i['_id'])
        stat_data = stat_data[0]
        history = []
        how_many_test = 0
        best_score = 0
        avg_score = 0
        for x in range (0,4,1):
            history.append(random.randint(0,40))
            how_many_test = how_many_test + 1

        best_score = max(history)
        avg_score = sum(history)/how_many_test
        stat_data = stat_data.update(history = history, how_many_test=how_many_test, best_score = best_score, avg_score=avg_score)


'''