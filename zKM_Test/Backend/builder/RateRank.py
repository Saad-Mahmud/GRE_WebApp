import abc
import operator

import six
from flask_login import current_user

from zKM_Test.Backend.app import db
from zKM_Test.Backend.app.model import Gre_data, User


class RateRank:

    def __init__(self):
        pass

    def rating(self,username):
        rate = Gre_data.objects(username=username)
        rate = rate[0]
        return rate

    def ranking(self,ajax_var):
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
                dict2 = LocalNone()
                dict2 = dict2.localnone(dict1,i,user)
            else:
                dict2 = LocalCountry()
                dict2 = dict2.localcountry(dict1,i,user,ajax_var)

        sorted_global = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)

        sorted_local = sorted(dict2.items(), key=operator.itemgetter(1), reverse=True)
        # print(sorted_global,sorted_local)
        return sorted_global, sorted_local


class LocalNone:
    def localnone(self,dict1,i,user):
        if user.country == current_user.country:
            try:
                dict1[i['_id']] = i['rating']
            except:
                dict1[i['_id']] = 0

        return dict1


class LocalCountry:
    def localcountry(self,dict1,i,user,ajax_var):
        if user.country == ajax_var:
            try:
                dict1[i['_id']] = i['rating']
            except:
                dict1[i['_id']] = 0

        return dict1