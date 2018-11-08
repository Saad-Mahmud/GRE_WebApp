#factory pattern
from zMA_Test.Backend.app.model import user_word_history
from zMA_Test.Backend.practice.factory_pattern import LevelFactory
from zSaad_Test.Backend.Words.Words import Words
from zSaad_Test.Backend.Words.Words_Rating import Words_Rating


class Mode(object):
    def __init__(self):
        self.allWordsRatings = Words_Rating.objects()
        self.allWords = Words.objects()
        #self.alreadySeenWords = user_word_history.objects(username="moumita")[0]

    def set(self,type,username): pass


class PracticeMode(Mode):

    def set(self,type,username):
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
            return new_list[0:10]
        else:
            return sorted_ratings[0:10]


class TestMode(Mode):
    def set(self,type,username='amit'):
        factory = LevelFactory()
        sorted_ratings = factory.setlevel(type).set()
        return sorted_ratings[0:10]


class ModeFactory:

    def setmode(self, modeType):
        if modeType =="practice":
            return PracticeMode()
        elif modeType == "test":
            return TestMode()




"""
Provide a unified interface to a set of interfaces in a subsystem.
Facade defines a higher-level interface that makes the subsystem easier
to use.
"""


class Facade:
    """
    Know which subsystem classes are responsible for a request.
    Delegate client requests to appropriate subsystem objects.
    """

    def __init__(self):
        self._subsystem_1 = Subsystem1()
        self._subsystem_2 = Subsystem2()

    def operation(self):
        self._subsystem_1.operation1()
        self._subsystem_1.operation2()
        self._subsystem_2.operation1()
        self._subsystem_2.operation2()


class Subsystem1:
    """
    Implement subsystem functionality.
    Handle work assigned by the Facade object.
    Have no knowledge of the facade; that is, they keep no references to
    it.
    """

    def operation1(self):
        pass

    def operation2(self):
        pass


class Subsystem2:
    """
    Implement subsystem functionality.
    Handle work assigned by the Facade object.
    Have no knowledge of the facade; that is, they keep no references to
    it.
    """

    def operation1(self):
        pass

    def operation2(self):
        pass


def main():
    facade = Facade()
    facade.operation()