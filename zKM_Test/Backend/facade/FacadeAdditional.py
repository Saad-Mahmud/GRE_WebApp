from datetime import datetime

from flask import render_template, url_for, request, redirect, flash

from zKM_Test.Backend.app.model import User, Gre_data
from zMA_Test.Backend.test.fetch_test import create_session_test, create_gre_test, update_gre_data, create_test_summary
from zMA_Test.Backend.practice.fetch_practice import create_user_word_history

class Addition:
    def additionalInfo(self,username,form):
        user = User.objects(username=username)
        name = username
        check1 = CheckUser()
        check1 = check1.check(user=user)
        if check1:
            return True
        user = user[0]
        checkin = CheckUser()
        checkin = checkin.check2(user=user, form=form, name=name)
        if checkin == True:
            return True
        else:
            return False


class CheckUser:
    def check(self,user):
        if len(user) == 0:
            return True

    def check2(self,user, form, name):
        if user.check_password(form.confirm_password.data):
            user = user.update(age=form.age.data,
                               country=request.form.get('cnt_name'),
                               gender=form.gender.data)

            date = datetime.utcnow()
            create_gre_test(name, {}, date, 0, 0.0, 0.0, 0.0, request.form.get('cnt_name'), [], [], [])
            create_user_word_history(name)
            print('aaaaaaaaaaaaaaaaaaaaaaaaa',create_test_summary(name, []))
            flash("Congrats!!you can now log in !!!")
            return True
        else:
            return False