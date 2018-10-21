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
for x in range(1,11,1):
    t = random.randint(0,100)
    b = random.randint(0,100)
    a = random.randint(0,100)

    gre_record = Gre_data(username = str(x),how_many_test=str(t), best_score = b, avg_score = str(a))
    gre_record.save()
if __name__== "__main__":
    app.run(debug=True)