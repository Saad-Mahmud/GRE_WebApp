
from werkzeug.security import generate_password_hash
from datetime import datetime

from zKM_Test.Backend.app.model import User
from zMA_Test.Backend.test.fetch_test import create_gre_test
from zMA_Test.Backend.practice.fetch_practice import create_user_word_history, create_review_words

def init_admin_db():
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
