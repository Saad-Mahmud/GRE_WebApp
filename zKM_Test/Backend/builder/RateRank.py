import abc
import operator

import six
from flask_login import current_user

from zKM_Test.Backend.app import db
from zKM_Test.Backend.app.model import Gre_data, User


class RateRank:
    def rating(username):
        rate = Gre_data.objects(username=username)
        rate = rate[0]
        return rate

# class Director:
#     def __init__(self):
#         self._builder = None
#
#     def SetBuilder(self,builderObj):
#         self.builder = builderObj
#
#     def construct(self, ajax_var):
#         self.ajax_var = ajax_var
#         self._builder.xxx()
#
# @six.add_metaclass(abc.ABCMeta)
# class Builder:
#     @abc.abstractmethod
#     def xxx(self):
#         pass
#
#
# class ConcreteBuilder(Builder):
#     def __init__(self):
#         self.product=None
#
#     def xxx(self):
#         pass
#
#     def getProduct(self):
#         self.Product_object = Product(self)
#         return self.Product_object
#
# class Product:
#     def UseProduct(self):
#         print("ranking local and global")
#

    def ranking(ajax_var):
        col = db['gre_data']
        curser = col.find({})
        dict = {}
        dict1 = {}
        for i in curser:
            try:
                dict[i['_id']] = i['rating']
            except:
                dict[i['_id']] = 0
            user = User.objects(username=i['_id'])
            user = user[0]
            if ajax_var is None or ajax_var == 'select country' or ajax_var == current_user.country:
                if user.country == current_user.country:
                    try:
                        dict1[i['_id']] = i['rating']
                    except:
                        dict1[i['_id']] = 0
            else:
                if user.country == ajax_var:
                    try:
                        dict1[i['_id']] = i['rating']
                    except:
                        dict1[i['_id']] = 0
        sorted_global = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

        sorted_local = sorted(dict1.items(), key=operator.itemgetter(1), reverse=True)
        # print(sorted_global,sorted_local)
        return sorted_global, sorted_local
