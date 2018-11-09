import abc,os
from datetime import datetime

import six
from PIL import Image
from werkzeug.security import generate_password_hash

from App_Main.Backend.App import APP_MAIN
from zKM_Test.Backend.app.model import User
# from zKM_Test.Backend.app.routes_KM import save_pic


class Director:
    def __init__(self, form):
        self._builder = None
        self.pic = form.pic.data
        self.about_me = form.about_me.data

    # def SetBuilder(self,builderObj):
    #     self.builder = builderObj

    def construct(self,builder):
        #self.builder.Create()
        self._builder = builder
        self._builder.setPic(self.pic)
        self._builder.setAboutMe(self.about_me)
        self._builder.getProduct()

@six.add_metaclass(abc.ABCMeta)
class Builder:
    def __init__(self):
        self.pic = ''
        self.about_me = ''
        self.product = Product(self.pic, self.about_me)
    # @abc.abstractmethod
    # def Create(self):
    #     pass
    @abc.abstractmethod
    def setPic(self,pic):
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
    def save_pic(self,form_picture):

        random_hex = os.urandom(8).hex()
        _,f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(APP_MAIN.static_folder, 'img', picture_fn)
        output_size=(125,125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn


    def setPic(self,pic):
        self.pic = self.save_pic(pic)
    def setAboutMe(self,aboutme):
        self.about_me = aboutme

    def getProduct(self):
        self.product = Product(self.pic,self.about_me)
        #return User(username=self.username,email=self.email,password_hash=self.password_hash,reg_date=self.reg_date,usertype=self.usertype,about_me=self.about_me)

class Product(object):
    def __init__(self,pic,about_me):
        self.pic = pic
        self.about_me = about_me


