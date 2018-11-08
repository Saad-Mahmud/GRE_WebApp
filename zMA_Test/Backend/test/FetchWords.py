"""
from zMA_Test.Backend.test.abstract_factory_pattern import ModeFactory
from zSaad_Test.Backend.initDB.Words import Words_Test


class FetchWords2():
    def __init__(self):
        self.allWords = Words_Test.objects()

    def practice_words(self, type, mode):
        final_list = []
        modefactory = ModeFactory()
        rated_words = modefactory.setmode(mode).set(type)
        words_dict = self.allWords



        for w1 in rated_words:
            for w2 in words_dict:
                if w1['wordID'] == w2.wordID:
                    final_list.append([w2.wordID, w2.word, w2.meanings, w2.usages, w2.translations, w2.TYPE])
        return final_list


    """