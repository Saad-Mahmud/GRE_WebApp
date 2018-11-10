from flask_login import current_user

from zKM_Test.Backend.app.model import User


# class Adapter:
#     def Adapting(self,user):
#         if user.pic is not None:
#             current_user.update(pic=user.pic)
#         current_user.update(about_me=user.about_me)


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


class Adaptee:
    """
    Define an existing interface that needs adapting.
    """

    def specific_request(self,user):
        if user.pic is not None:
            current_user.update(pic=user.pic)
        current_user.update(about_me=user.about_me)
