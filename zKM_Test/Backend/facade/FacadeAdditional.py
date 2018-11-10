from datetime import datetime

from flask import render_template, url_for, request, redirect, flash

from zKM_Test.Backend.app.model import User, Gre_data
from zMA_Test.Backend.test.fetch_test import create_session_test, create_gre_test, update_gre_data, create_test_summary
from zMA_Test.Backend.practice.fetch_practice import create_user_word_history, create_review_words


class Addition:
    def __init__(self,username,form):
        self.user = User.objects(username=username)
        self.name = username
        self.form = form

    def additionalInfo(self):
        check1 = CheckUser()
        check1 = check1.check(user=self.user)
        if check1:
            return True
        self.user = self.user[0]
        checkin = CheckUser()
        checkin = checkin.check2(user=self.user, form=self.form, name=self.name)
        if checkin == True:
            return True
        else:
            return False


class CheckUser:
    def check(self,user):
        self.user = user
        if len(self.user) == 0:
            return True

    def check2(self,user, form, name):
        self.user = user
        self.form = form
        self.name = name
        if self.user.check_password(self.form.confirm_password.data):
            self.user = self.user.update(age=self.form.age.data,
                               country=request.form.get('cnt_name'),
                               gender=self.form.gender.data)

            self.date = datetime.utcnow()
            create_gre_test(self.name, {}, self.date, 0, 0.0, 0.0, 0.0, request.form.get('cnt_name'), [], [], [])
            create_user_word_history(self.name)
            create_review_words(self.name, [])
            print('aaaaaaaaaaaaaaaaaaaaaaaaa',create_test_summary(self.name, []))
            flash("Congrats!!you can now log in !!!")
            return True
        else:
            return False