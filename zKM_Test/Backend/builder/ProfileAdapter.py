from flask_login import current_user

from zKM_Test.Backend.app.model import User


class Adapter:
    def Adapting(self,user):
        if user.pic is not None:
            current_user.update(pic=user.pic)
        current_user.update(about_me=user.about_me)
