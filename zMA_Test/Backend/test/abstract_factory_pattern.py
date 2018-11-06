#factory pattern
from zMA_Test.Backend.app.model import user_word_history
from zMA_Test.Backend.practice.factory_pattern import LevelFactory
from zSaad_Test.Backend.initDB.words import Words_Rating, Words_Test


class Mode(object):
    def __init__(self):
        self.allWordsRatings = Words_Rating.objects()
        self.allWords = Words_Test.objects()
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
                    print("sorted ratings words ", word['wordID'], word['Ratings'])

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

