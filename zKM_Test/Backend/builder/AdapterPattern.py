import abc

import six

from zKM_Test.Backend.app.model import User



@six.add_metaclass(abc.ABCMeta)
class Target:
    """
    Define the domain-specific interface that Client uses.
    """

    def __init__(self):
        self._adaptee = Adaptee()

    @abc.abstractmethod
    def request(self):
        pass


class Adapter(Target):
    """
    Adapt the interface of Adaptee to the Target interface.
    """

    def request(self,user):
        self.user1 = self._adaptee.specific_request(user)
        return self.user1

class Adaptee:
    """
    Define an existing interface that needs adapting.
    """

    def specific_request(self,user):
      self.user =  User(username=user.username,
                             email=user.email,
                             password_hash=user.password_hash,reg_date=user.reg_date, usertype=user.usertype,
                             about_me=user.about_me)

      return self.user

# class Adapter:
#     def Adapting(self,user):
#         self.user1 = User(username=user.username,
#                      email=user.email,
#                      password_hash=user.password_hash,reg_date=user.reg_date, usertype=user.usertype,
#                      about_me=user.about_me)
#         return self.user1