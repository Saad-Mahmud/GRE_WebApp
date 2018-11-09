from flask import url_for, redirect, request
from flask_login import login_user
from werkzeug.urls import url_parse

from zKM_Test.Backend.app.model import User


class LoginFactory:

    def __init__(self):
        pass

    def CheckValid(self,form):
        self.str = ''
        self.form = form

        self.user = User.objects(username=form.username.data)
        if len(self.user)== 0:
           self.str = "invalid"
        else:
           self.str = "proceed"
        self.strcheck = stringcheck()
        self.strcheck = self.strcheck.StrCheck(self.str,self.user,self.form)
        return self.strcheck


class stringcheck:

    def StrCheck(self,str,user,form):
        self.str = str
        self.user = user
        self.form = form

        self.red = Redirect()
        if self.str=='invalid':
            self.redd = self.red.BackToLogin()
            return self.redd
        if self.str == 'proceed':
            self.redd = self.red.Proceed(self.user, self.form)
            return self.redd


class Redirect:

    def BackToLogin(self):
        return url_for('login')

    def Proceed(self,user,form):
        self.user = user
        self.form = form
        self.user = self.user[0]
        if self.user is None or not self.user.check_password(self.form.password.data):
            self.BackToLogin()
        login_user(self.user,remember=self.form.remember_me.data)
        self.next_page = request.args.get('next')
        if not self.next_page or url_parse(self.next_page).netloc !='':
            self.next_page = url_for('index')

        return self.next_page