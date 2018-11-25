
import pymongo
from flask import Flask
from werkzeug.security import generate_password_hash
from mongoengine import *
from datetime import datetime

from zKM_Test.Backend.app.model import User
from zMA_Test.Backend.test.fetch_test import create_gre_test
from zMA_Test.Backend.practice.fetch_practice import create_user_word_history, create_review_words

#
#
# class Country(UserMixin, Document):
#     country_id = IntField(required=True, primary_key=True)
#     country_name = StringField(required=True, max_length=50, unique=True)
'''
app = Flask(__name__)

client = pymongo.MongoClient("localhost",27017)
db = client.zSaad_Test
connect('zSaad_Test', host="127.0.0.1", port = 27017)

cntttt = ["America","Argentina","Australia","Bangladesh","Brazil","China","England",
          "Honululu","India","Japan", "Nepal","Pakistan",
          "Russia","Sri Lanka","Syria","Uganda"
          ]
pword = 'admin'
user = User(username='admin',
            email='admin@gmail.com',
            password_hash=generate_password_hash(pword),
            country = cntttt[3],
            about_me = "admin\'s about",
            age = "20",
            reg_date = datetime.utcnow(),
            gender = 'Male'
            ,usertype = 'A'  #for admin, it is 'A', for others, 'U'
            )

user.save()
create_gre_test("admin", {}, datetime.utcnow(), 0, 0.0, 0.0, 0.0, "Bangladesh", [], [], [])
create_user_word_history("admin")
create_review_words("admin", [])


#
# col = db['user']
# cursor = col.find({})
# lastweek = datetime.now()
# for i in cursor:
#     #if i['usertype']=='A':
#         gre_record = Gre_data(username=i['_id'])
#         print(gre_record.username)
#         gre_record.save()
#         stat_data = Gre_data.objects(username=i['_id'])
#         stat_data = stat_data[0]
#         history = []
#         rating_chart = []
#         rate_date = []
#         how_many_test = 0
#         rating = 0
#         for x in range (0,4,1):
#             a = random.randint(0,40)
#             b = random.randint(100, 200)
#             history.append(a)
#             rating_chart.append(b)
#             lastweek = lastweek + timedelta(days=1)
#             rate_date.append(lastweek)
#             how_many_test = how_many_test + 1
#             rating = rating + a
#
#         best_score = max(history)
#         avg_score = rating/how_many_test
#         user = User.objects(username=i['_id'])
#         user = user[0]
#         country = user.country
#         stat_data = stat_data.update(history = history, how_many_test=how_many_test,rating = rating, best_score = best_score, avg_score=avg_score, test_date=datetime.utcnow(), country=country,
#                                      rate_date=rate_date, rating_chart=rating_chart)
#
#
#
# for i in range(1,17,1):
#     cnt = Country(country_id=i,
#                   country_name=cntttt[i-1])
#     cnt.save()
#
#
# collection = db['country']
# cursor = collection.find({})
# for i in cursor:
#     print(i['country_name'])
#


# from flask import Flask
# import os
# app = Flask(__name__)
#
# a = os.environ.get('DBPASS')
# b = os.environ.get('DBUSER')
#
# print(a)
# print(b)


'''