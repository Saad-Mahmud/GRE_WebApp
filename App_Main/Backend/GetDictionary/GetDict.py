from App_Main.Backend.DictionaryMaker.AnonDict import AnonDict
from App_Main.Backend.DictionaryMaker.AdminDict import AdminDict
from App_Main.Backend.DictionaryMaker.UserDict import UserDict


class GetDict():

    def __init__(self):

        self.udict = UserDict()
        self.adict = AdminDict()
        self.andict = AnonDict()

    def get_userdict(self,userID,query):
        self.udict.setUser(userID)
        self.udict.fetch_words(query)
        self.udict.build()
        return  self.udict.get()

    def get_adict(self,query):
        self.adict.fetch_words(query)
        self.adict.build()
        return  self.adict.get()

    def get_andict(self,query):
        self.andict.fetch_words(query)
        return  self.andict.get()