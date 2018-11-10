from zMA_Test.Backend.app.model import session_practice, user_word_history, review_words
from zMA_Test.Backend.test.test_factory_pattern import ModeFactory
from App_Main.Backend.Words.Words import Words


def create_session_practice(status, words, idx, edited_words):
    session = session_practice(status=status, words=words, idx=idx, edited_words=edited_words)
    session2 = session.save()
    return session2


def create_user_word_history(username):
    wordHistory = user_word_history(username)
    wordHistory2 = wordHistory.save()
    return wordHistory2


def update_user_word_status(oldStatus, newStatus):
    mergedList = newStatus + [s for s in oldStatus if s not in oldStatus]
    return mergedList


def create_review_words(username, summary):
    sum = review_words(username=username, summary=summary)
    sum = sum.save()
    return sum


def update_review_words(username, words):
    prev_sum = words
    practice_sum = review_words.objects(username=username)[0]
    practice_sum.summary.append(prev_sum)
    practice_sum.save()
    return prev_sum


class FetchWords():
    def __init__(self,username):
        self.allWords = Words.objects()
        self.username = username

    def practice_words(self, type, mode):
        final_list = []
        modefactory = ModeFactory()
        rated_words = modefactory.setmode(mode).set(type, self.username)
        words_dict = self.allWords

        for w1 in rated_words:
            for w2 in words_dict:
                if w1['wordID'] == w2.wordID:
                    final_list.append(
                        {
                            'wordID': w2.wordID,
                            'word': w2.word,
                            'TYPE': w2.TYPE,
                            'meaning': w2.meanings[0],
                            'usage': w2.usages[0],
                            'translations': w2.translations
                        })
        return final_list



def fetch_session_practice(sessionID):
    return session_practice.objects(id=sessionID)[0]


def fetch_user_word_history(username):
    return user_word_history.objects(username=username)[0]

def fetch_review_words(username):
    return review_words.objects(username=username)[0]


