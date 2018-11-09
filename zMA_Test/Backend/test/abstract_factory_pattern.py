#factory pattern
import six

from zMA_Test.Backend.app.model import user_word_history
from zMA_Test.Backend.practice.factory_pattern import LevelFactory
from App_Main.Backend.Words.Words import Words
from App_Main.Backend.Words.Words_Rating import Words_Rating

#
# class Mode(object):
#     def __init__(self):
#         self.allWordsRatings = Words_Rating.objects()
#         self.allWords = Words.objects()
#         #self.alreadySeenWords = user_word_history.objects(username="moumita")[0]
#
#     def set(self,type,username): pass
#
#
# class PracticeMode(Mode):
#
#     def set(self,type,username):
#         alreadySeenWords = user_word_history.objects(username=username)[0]
#         factory = LevelFactory()
#         sorted_ratings = factory.setlevel(type).set()
#         new_list = []
#
#         for word in sorted_ratings:
#             if word['wordID'] not in alreadySeenWords.status:
#                 new_list.append(word)
#             else:
#                 if alreadySeenWords.status[word['wordID']] != 'green':
#                     new_list.append(word)
#                     print("sorted ratings Words ", word['wordID'], word['Ratings'])
#
#         if len(new_list) >= 10:
#             return new_list[0:10]
#         else:
#             return sorted_ratings[0:10]
#
#
# class TestMode(Mode):
#     def set(self,type,username='amit'):
#         factory = LevelFactory()
#         sorted_ratings = factory.setlevel(type).set()
#         return sorted_ratings[0:10]
#
#
# class ModeFactory:
#
#     def setmode(self, modeType):
#         if modeType =="practice":
#             return PracticeMode()
#         elif modeType == "test":
#             return TestMode()
#
#
#

#
# """
# Define an interface for creating an object, but let subclasses decide
# which class to instantiate. Factory Method lets a class defer
# instantiation to subclasses.
# """
#
import abc


@six.add_metaclass(abc.ABCMeta)
class Mode():
    """
    Declare the factory method, which returns an object of type Product.
    Creator may also define a default implementation of the factory
    method that returns a default ConcreteProduct object.
    Call the factory method to create a Product object.
    """

    def __init__(self,country_id=0):
        self.product = self.factory_method()

    @abc.abstractmethod
    def factory_method(self):
        pass



class TestMode(Mode):
    """
    Override the factory method to return an instance of a
    ConcreteProduct1.
    """

    def factory_method(self):
        return TestProduct()


class PracticeMode(Mode):
    """
    Override the factory method to return an instance of a
    ConcreteProduct2.
    """

    def factory_method(self):
        return PracticeProduct()


@six.add_metaclass(abc.ABCMeta)
class Product():
    """
    Define the interface of objects the factory method creates.
    """
    def __init__(self):
        self.allWordsRatings = Words_Rating.objects()
        self.allWords = Words.objects()

    @abc.abstractmethod
    def set(self,type, username,no_of_words=3):
        pass


class TestProduct(Product):
    """
    Implement the Product interface.
    """

    def set(self,type,username='amit',no_of_words=3):
        factory = LevelFactory()
        sorted_ratings = factory.setlevel(type).set()
        return sorted_ratings[0:10]


class PracticeProduct(Product):
    """
    Implement the Product interface.
    """

    def set(self,type,username,no_of_words=3):
        alreadySeenWords = user_word_history.objects(username=username)[0]
        factory = LevelFactory()
        sorted_ratings = factory.setlevel(type).set()
        new_list = []

        for word in sorted_ratings:
            if word['wordID'] not in alreadySeenWords.status:
                new_list.append(word)
            else:
                if alreadySeenWords.status[word['wordID']] != 'green':
                    new_list.append(word)
                    print("sorted ratings Words ", word['wordID'], word['Ratings'])

        if len(new_list) >= 10:
            return new_list[0:no_of_words]
        else:
            return sorted_ratings[0:no_of_words]


class ModeFactory:

    def setmode(self, modeType):
        if modeType =="practice":
            creator = PracticeMode()
        else:
            creator = TestMode()
        return creator.factory_method()


