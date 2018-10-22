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

cntttt = ["Bangladesh","America","England","Syria","Uganda","Honululu","India","Pakistan","Brazil","Argentina"]
pword = 'abc'
for i in range(1,11,1):
    x = random.randint(0,5)
    user = User(username=str(i),
                email=str(i)+'@gmail.com',
                password_hash=generate_password_hash(pword),
                country = cntttt[x]
                )
    user.save()
    gre_record = Gre_data(username=str(i))
    gre_record.save()


for i in range(1,11,1):
    cnt = Country(country_id=i,
                  country_name=cntttt[i-1])
    cnt.save()

collection = db['country']
cursor = collection.find({})
for i in cursor:
    print(i['country_name'])

if __name__== "__main__":
    app.run(debug=True)

