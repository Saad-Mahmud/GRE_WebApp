from zMA_Test.Backend.app.model import session_practice, user_word_history
from zMA_Test.Backend.test.abstract_factory_pattern import ModeFactory
from zSaad_Test.Backend.words.Words import Words


def create_session_practice(status, words, idx):
    session = session_practice(status=status, words=words, idx=idx)
    session2 = session.save()
    return session2


def create_user_word_history(username):
    #wordHistory = user_word_history("moumita")
    wordHistory = user_word_history(username)
    wordHistory2 = wordHistory.save()
    return wordHistory2


def update_user_word_status(oldStatus, newStatus):
    mergedList = newStatus + [s for s in oldStatus if s not in oldStatus]
    return mergedList



class FetchWords():

    def __init__(self,username):
        self.allWords = Words.objects()
        print('sellllllllllllffffff', self.allWords)
        self.username = username

    def practice_words(self, type, mode):
        final_list = []
        modefactory = ModeFactory()
        rated_words = modefactory.setmode(mode).set(type, self.username)

        #rated_words = self.practice_ratings(type)
        words_dict = self.allWords

        print('rated ', rated_words)
        print('words_dict ', words_dict)

        for w1 in rated_words:
            for w2 in words_dict:
                if w1['wordID'] == w2.wordID:
                    #print("meaningggggg : ", w2.word, w2.meanings)
                    print('w1', w1)
                    print('w2', w2)
                    final_list.append(
                        {
                            'wordID': w2.wordID,
                            'word': w2.word,
                            'TYPE': w2.TYPE,
                            'meaning': w2.meanings[0],
                            'usage': w2.usages[0],
                            'translations': w2.translations
                        })

        print("baaaaaaaaaaaaaaaa ", final_list)

        return final_list







