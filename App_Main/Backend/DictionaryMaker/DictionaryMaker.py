import abc
import six

from App_Main.Backend.DictionaryCard.Usage import Usage
from App_Main.Backend.DictionaryCard.ConcreteCard import ConcreteCard
from App_Main.Backend.DictionaryCard.Meaning import Meaning
from App_Main.Backend.Words.Words import Words


@six.add_metaclass(abc.ABCMeta)
class DictionaryMaker():
    """
    Declare the factory method, which returns an object of type Product.
    Creator may also define a default implementation of the factory
    method that returns a default ConcreteProduct object.
    Call the factory method to create a Product object.
    """

    def __init__(self):
        self.words = []
        self.dict = {}
        self.query = None
        self.userid = None


    @abc.abstractmethod
    def build(self):
        pass

    @abc.abstractmethod
    def get(self):
        pass

    def fetch_words(self, letter):
        self.query = letter
        if(self.query == 'all'):
            self.words = Words.objects
        else:
            self.words = Words.objects(wordID__startswith=self.query)
        for w in self.words:
            self.dict[w.wordID] = ConcreteCard(w.wordID, w.TYPE, w.word)
            self.dict[w.wordID] = Meaning(self.dict[w.wordID])
            self.dict[w.wordID].setData(w.meanings[0])
            self.dict[w.wordID] = Usage(self.dict[w.wordID])
            self.dict[w.wordID].setData(w.usages)


