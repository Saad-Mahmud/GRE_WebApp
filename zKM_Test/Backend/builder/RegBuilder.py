import abc
from datetime import datetime

import six
from werkzeug.security import generate_password_hash

from zKM_Test.Backend.app.model import User


class Director:
    def __init__(self, form):
        self._builder = None
        self.username = form.username.data
        self.email = form.email.data
        self.password_hash = generate_password_hash(form.password.data)
        self.reg_date = datetime.utcnow()
        self.usertype = 'U'
        self.about_me = form.username.data+"\'s about"

    # def SetBuilder(self,builderObj):
    #     self.builder = builderObj

    def construct(self,builder):
        #self.builder.Create()
        self._builder = builder
        self._builder.setUsername(self.username)
        self._builder.setEmail(self.email)

        self._builder.setPassword(self.password_hash)
        self._builder.setRegDate(self.reg_date)
        self._builder.setUsertype(self.usertype)
        self._builder.setAboutMe(self.about_me)
        self._builder.getProduct()

@six.add_metaclass(abc.ABCMeta)
class Builder:
    def __init__(self):
        self.username = ''
        self.email = ''
        self.password_hash = ''
        self.reg_date = datetime.utcnow()
        self.usertype = ''
        self.about_me = ''
        self.product = Product(self.username, self.email, self.password_hash, self.reg_date, self.usertype, self.about_me)
    # @abc.abstractmethod
    # def Create(self):
    #     pass
    @abc.abstractmethod
    def setUsername(self,username):
        pass
    @abc.abstractmethod
    def setEmail(self,email):
        pass

    @abc.abstractmethod
    def setPassword(self,password):
        pass
    @abc.abstractmethod
    def setRegDate(self,regdate):
        pass

    @abc.abstractmethod
    def setUsertype(self,usertype):
        pass
    @abc.abstractmethod
    def setAboutMe(self,aboutme):
        pass
    @abc.abstractmethod
    def getProduct(self):
        pass

class ConcreteBuilder(Builder):
    # def Create(self):
    #     self.product = Product()

    def setUsername(self,username):
        self.username = username
    def setEmail(self,email):
        self.email = email

    def setPassword(self,password):
        self.password_hash = password
    def setRegDate(self,regdate):
        self.reg_date = regdate

    def setUsertype(self,usertype):
        self.usertype = usertype
    def setAboutMe(self,aboutme):
        self.about_me = aboutme

    def getProduct(self):
        self.product = Product(self.username,self.email,self.password_hash,self.reg_date,self.usertype,self.about_me)
        #return User(username=self.username,email=self.email,password_hash=self.password_hash,reg_date=self.reg_date,usertype=self.usertype,about_me=self.about_me)

class Product(object):
    def __init__(self,username,email,password_hash,reg_date,usertype,about_me):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.reg_date = reg_date
        self.usertype = usertype
        self.about_me = about_me


