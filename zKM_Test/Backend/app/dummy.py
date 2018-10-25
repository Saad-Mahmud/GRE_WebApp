from datetime import datetime
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
    x = random.randint(0,3)
    user = User(username=str(i),
                email=str(i)+'@gmail.com',
                password_hash=generate_password_hash(pword),
                country = cntttt[x],
                about_me = str(i) + "\'s about",
                age = str(random.randint(1,30)),
                reg_date = datetime.utcnow(),
                gender = 'Male'
                ,usertype = 'U'  #for admin, it is 'A', for others, 'U'
                )
    user.save()

col = db['user']
cursor = col.find({})

for i in cursor:
    if i['usertype']=='U':
        gre_record = Gre_data(username=i['_id'])
        print(gre_record.username)
        gre_record.save()
        stat_data = Gre_data.objects(username=i['_id'])
        stat_data = stat_data[0]
        history = []
        how_many_test = 0
        rating = 0
        for x in range (0,4,1):
            a = random.randint(0,40)
            history.append(a)
            how_many_test = how_many_test + 1
            rating = rating + a

        best_score = max(history)
        avg_score = rating/how_many_test
        user = User.objects(username=i['_id'])
        user = user[0]
        country = user.country
        stat_data = stat_data.update(history = history, how_many_test=how_many_test,rating = rating, best_score = best_score, avg_score=avg_score, test_date=datetime.utcnow(), country=country)


'''
for i in range(1,11,1):
    cnt = Country(country_id=i,
                  country_name=cntttt[i-1])
    cnt.save()


collection = db['country']
cursor = collection.find({})
for i in cursor:
    print(i['country_name'])


from flask import Flask
import os
app = Flask(__name__)

a = os.environ.get('DBPASS')
b = os.environ.get('DBUSER')

print(a)
print(b)
'''
if __name__== "__main__":
    app.run(debug=True)

