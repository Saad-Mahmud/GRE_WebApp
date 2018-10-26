import operator

from zMA_Test.Backend.app.model import session_practice, user_word_history
from zSaad_Test.Backend.initDB.words import Words_Rating, Words_Test


def fetch_easy_rating(country_id=0):
    already_seen_words = user_word_history.objects(username="moumita")[0]
    temp_list = Words_Rating.objects()

    temps = [
        {
            'wordID': w.wordID,
            'Ratings': w.Ratings,

        }
        for w in temp_list
    ]

    sorted_temp = sorted(temps, key=lambda k: k['Ratings'][country_id])
    new_list = []

    for i in range(0, 333):
        if sorted_temp[i]['wordID'] not in already_seen_words.status:
            print("bla ")
            new_list.append(sorted_temp[i])

        else:
            if already_seen_words.status[sorted_temp[i]['wordID']]!='green':
                new_list.append(sorted_temp[i])
                print("maf chai ", sorted_temp[i]['wordID'])

    if len(new_list)>=10:
        return new_list[0:10]
    else:
        return sorted_temp[0:10]


def fetch_easy_words(country_id=0):
    final_list = []
    rated_words = fetch_easy_rating(country_id)
    words_dict = Words_Test.objects()

    for w1 in rated_words:
        for w2 in words_dict:
            if w1['wordID'] == w2.wordID:
                print("meaningggggg : ", w2.word, w2.meanings)
                # final_easy_list.append([w2.wordID, w2.word, w2.meanings, w2.usages, w2.translations, w2.TYPE ])
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


def create_session_practice(status, words, idx):
    session = session_practice(status=status, words=words, idx=idx)
    session2 = session.save()
    return session2


def create_user_word_history():
    wordHistory = user_word_history("moumita")
    wordHistory2 = wordHistory.save()
    return wordHistory2


def update_user_word_status(oldStatus, newStatus):
    mergedList = newStatus + [s for s in oldStatus if s not in oldStatus]
    return mergedList


class FetchWords():
    def __init__(self):
        self.allWordsRatings = Words_Rating.objects()
        self.allWords = Words_Test.objects()
        self.alreadySeenWords = user_word_history.objects(username="moumita")[0]
        self.wordRatingList = [
        {
            'wordID': w.wordID,
            'Ratings': w.Ratings,

        }
        for w in self.allWordsRatings
    ]

    def sorted_words(self, type, country_id=0):
        sorted_ratings = sorted(self.wordRatingList, key=lambda k: k['Ratings'][country_id])
        if type=="easy":
            sorted_ratings = sorted_ratings[0:333]
        elif type=="medium":
            sorted_ratings = sorted_ratings[334:666]
        elif type=="hard":
            sorted_ratings = sorted_ratings[667:1000]
        return sorted_ratings

    def practice_ratings(self, type):
        new_list = []
        sorted_ratings = self.sorted_words(type)
        for word in sorted_ratings:
            if word['wordID'] not in self.alreadySeenWords.status:
                new_list.append(word)
            else:
                if self.alreadySeenWords.status[word['wordID']] != 'green':
                    new_list.append(word)
                    print("sorted ratings words ", word['wordID'])

        if len(new_list) >= 10:
            return new_list[0:10]
        else:
            return sorted_ratings[0:10]

    def practice_words(self, type):
        final_list = []
        rated_words = self.practice_ratings(type)
        words_dict = self.allWords

        for w1 in rated_words:
            for w2 in words_dict:
                if w1['wordID'] == w2.wordID:
                    print("meaningggggg : ", w2.word, w2.meanings)
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







