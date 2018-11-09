import abc
import operator

import six
from flask_login import current_user

from App_Main.Backend.App import db
from zKM_Test.Backend.app.model import Gre_data, User


class RateRank:

    def __init__(self):
        pass

    def rating(self,username):
        rate = Gre_data.objects(username=username)
        rate = rate[0]
        return rate

    def ranking(self,ajax_var):
        self.str = ''
        col = db['gre_data']
        curser = col.find({})
        self.dict = {}
        self.dict1 = {}
        for i in curser:
            try:
                self.dict[i['_id']] = i['rating']
            except:
                self.dict[i['_id']] = 0
            self.user = User.objects(username=i['_id'])
            self.user = self.user[0]
            # if ajax_var is None or ajax_var == 'select country' or ajax_var == current_user.country:
            #     if user.country == current_user.country:
            #         try:
            #             dict1[i['_id']] = i['rating']
            #         except:
            #             dict1[i['_id']] = 0
            # else:
            #     if user.country == ajax_var:
            #         try:
            #             dict1[i['_id']] = i['rating']
            #         except:
            #             dict1[i['_id']] = 0
            if ajax_var is None or ajax_var == 'select country' or ajax_var == current_user.country:
                self.str = 'local'
                self.dict2 = LocalRank()
                self.dict2 = self.dict2.localrank(self.str, self.dict1, i, self.user, ajax_var)
                # dict2 = LocalNone()
                # dict2 = dict2.localnone(dict1,i,user)
            else:
                self.str = 'other'
                self.dict2 = LocalRank()
                self.dict2 = self.dict2.localrank(self.str,self.dict1, i, self.user, ajax_var)
                # dict2 = LocalCountry()
                # dict2 = dict2.localcountry(dict1,i,user,ajax_var)

        sorted_global = sorted(self.dict.items(), key=operator.itemgetter(1), reverse=True)

        sorted_local = sorted(self.dict2.items(), key=operator.itemgetter(1), reverse=True)
        # print(sorted_global,sorted_local)
        return sorted_global, sorted_local


class LocalRank:
    def localrank(self, str, dict1, i, user, ajax_var):
        self.str = str
        self.dict1 = dict1
        self.i = i
        self.user = user
        self.ajax_var = ajax_var
        if str == 'local':
            dict2 = LocalNone()
            return dict2.localnone(self.dict1, self.i, self.user)
        elif str == 'other':
            dict2 = LocalCountry()
            return dict2.localcountry(self.dict1, self.i, self.user, self.ajax_var)

class LocalNone:
    def localnone(self,dict1,i,user):
        self.dict1 = dict1
        self.i = i
        self.user = user
        if self.user.country == current_user.country:
            try:
                self.dict1[self.i['_id']] = self.i['rating']
            except:
                self.dict1[self.i['_id']] = 0

        return self.dict1


class LocalCountry:
    def localcountry(self,dict1,i,user,ajax_var):
        self.dict1 = dict1
        self.i = i
        self.user = user
        if self.user.country == ajax_var:
            try:
                self.dict1[self.i['_id']] = self.i['rating']
            except:
                self.dict1[self.i['_id']] = 0

        return self.dict1