from zKM_Test.Backend.app.model import User


class Adapter:
    def Adapting(self,user):
        user1 = User(username=user.username,
                     email=user.email,
                     password_hash=user.password_hash,reg_date=user.reg_date, usertype=user.usertype,
                     about_me=user.about_me)
        return user1