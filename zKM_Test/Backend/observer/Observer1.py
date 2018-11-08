from flask import flash
from flask_login import current_user


class Subscriber:

    def __init__(self,name):
        self.name = name

    def update(self,message):

        print('{} got message "{}"'.format(self.name,message))
        flash('{} got message "{}"'.format(self.name,message))


class Publisher:

    def __init__(self):
        self.subscribers = set()

    def register(self, who):
        self.subscribers.add(who)

    def unregister(self,who):
        self.subscribers.discard(who)

    def dispatch(self,message):
        print(message)
        for subscriber in self.subscribers:
            subscriber.update(message)

class Notification:
    def Ovserved(self):
        pub = Publisher()
        user = Subscriber(current_user.username)
        pub.register(user)
        pub.dispatch("Your rating Has been Updated!!!Carry on!!!")
