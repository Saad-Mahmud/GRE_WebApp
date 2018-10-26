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
        new_list = []
        sorted_ratings = self.sorted_words(type)
        '''for word in sorted_ratings:
            if word['wordID'] not in self.alreadySeenWords.status:
                new_list.append(word)
            else:
                if self.alreadySeenWords.status[word['wordID']] != 'green':
                    new_list.append(word)
                    print("sorted ratings words ", word['wordID'])

        if len(new_list) >= 10:
            return new_list[0:10]
        else:
            return sorted_ratings[0:10]'''
        return sorted_ratings[0:10]

    def practice_words(self, type):
        final_list = []
        rated_words = self.practice_ratings(type)
        words_dict = self.allWords

        for w1 in rated_words:
            for w2 in words_dict:
                if w1['wordID'] == w2.wordID:
                    #print("meaningggggg : ", w2.word, w2.meanings)
                    final_list.append([w2.wordID, w2.word, w2.meanings, w2.usages, w2.translations, w2.TYPE])
                    '''final_list.append(
                        {
                            'wordID': w2.wordID,
                            'word': w2.word,
                            'TYPE': w2.TYPE,
                            'meaning': w2.meanings[0],
                            'usage': w2.usages[0],
                            'translations': w2.translations
                        })'''

        return final_list