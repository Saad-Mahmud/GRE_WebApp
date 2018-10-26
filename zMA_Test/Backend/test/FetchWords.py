from zSaad_Test.Backend.initDB.words import Words_Rating, Words_Test


class FetchWords2():
    def __init__(self):
        self.allWordsRatings = Words_Rating.objects()
        self.allWords = Words_Test.objects()
        self.wordRatingList = [
            {
                'wordID': w.wordID,
                'Ratings': w.Ratings,

            }
            for w in self.allWordsRatings
        ]

    def sorted_words(self, type, country_id=0):
        sorted_ratings = sorted(self.wordRatingList, key=lambda k: k['Ratings'][country_id])
        if type == "easy":
            sorted_ratings = sorted_ratings[0:333]
        elif type == "medium":
            sorted_ratings = sorted_ratings[334:666]
        elif type == "hard":
            sorted_ratings = sorted_ratings[667:1000]
        return sorted_ratings

    def practice_ratings(self, type):
        sorted_ratings = self.sorted_words(type)
        return sorted_ratings[0:10]

    def practice_words(self, type):
        final_list = []
        rated_words = self.practice_ratings(type)
        words_dict = self.allWords

        for w1 in rated_words:
            for w2 in words_dict:
                if w1['wordID'] == w2.wordID:
                    final_list.append([w2.wordID, w2.word, w2.meanings, w2.usages, w2.translations, w2.TYPE])
        return final_list