import six

from App_Main.Backend.Words.Words_Rating import Words_Rating


#
# """
# Define an interface for creating an object, but let subclasses decide
# which class to instantiate. Factory Method lets a class defer
# instantiation to subclasses.
# """
#
import abc


@six.add_metaclass(abc.ABCMeta)
class Level():
    """
    Declare the factory method, which returns an object of type Product.
    Creator may also define a default implementation of the factory
    method that returns a default ConcreteProduct object.
    Call the factory method to create a Product object.
    """

    def __init__(self, country_id=0):
        self.product = self.factory_method()

    @abc.abstractmethod
    def factory_method(self):
        pass


class EasyLevel(Level):
    """
    Override the factory method to return an instance of a
    ConcreteProduct1.
    """

    def factory_method(self):
        return EasyProduct()


class MediumLevel(Level):
    """
    Override the factory method to return an instance of a
    ConcreteProduct2.
    """

    def factory_method(self):
        return MediumProduct()


class HardLevel(Level):
    """
    Override the factory method to return an instance of a
    ConcreteProduct2.
    """

    def factory_method(self):
        return HardProduct()


@six.add_metaclass(abc.ABCMeta)
class Product():
    """
    Define the interface of objects the factory method creates.
    """

    def __init__(self, country_id=0):
        self.allWordsRatings = Words_Rating.objects()
        self.wordRatingList = [
            {
                'wordID': w.wordID,
                'Ratings': w.Ratings,

            }
            for w in self.allWordsRatings
        ]
        self.sorted_ratings = sorted(self.wordRatingList, key=lambda k: k['Ratings'][country_id])

    @abc.abstractmethod
    def set(self):
        pass


class EasyProduct(Product):
    """
    Implement the Product interface.
    """

    def set(self):
        return self.sorted_ratings[0:333]


class MediumProduct(Product):
    """
    Implement the Product interface.
    """

    def set(self):
        return self.sorted_ratings[334:666]


class HardProduct(Product):
    """
    Implement the Product interface.
    """

    def set(self):
        return self.sorted_ratings[667:1000]


class LevelFactory:

    def setlevel(self, levelType):
        if levelType == "easy":
            creator = EasyLevel()
        elif levelType == "medium":
            creator = MediumLevel()
        else:
            creator = HardLevel()
        return creator.factory_method()
