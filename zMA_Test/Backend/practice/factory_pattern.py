from zSaad_Test.Backend.initDB.words import Words_Rating

#factory pattern


class Level(object):

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

    def set(self): pass


class EasyLevel(Level):
    def set(self):
        return self.sorted_ratings[0:333]


class MediumLevel(Level):
    def set(self):
        return self.sorted_ratings[334:666]


class HardLevel(Level):
    def set(self):
        return self.sorted_ratings[667:1000]


class LevelFactory:

    def setlevel(self, levelType):
        if levelType =="easy":
            return EasyLevel()
        elif levelType == "medium":
            return MediumLevel()
        elif levelType =="hard":
            return HardLevel()
"""
ff = levelFactory()
gg = ff.setLevel("easy")
gg.set()
"""

