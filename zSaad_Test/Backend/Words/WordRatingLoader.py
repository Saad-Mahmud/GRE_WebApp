import pandas as pd

from zSaad_Test.Backend.Words.CsvToRatingAdapter import CsvToRatingAdapter

class WordRatingLoader():

    def __init__(self,path):
        try:
            self.df = pd.read_csv(path, sep='|')
        except IOError as error:
            raise IOError

        self.size = self.df.shape[0]
        self.pointer = 0

    def hasNext(self):
        if(self.pointer>=self.size):return False
        return True

    def next_ratings(self):
        if(self.pointer>=self.size):
            raise IndexError

        this_word = self.df.iloc[self.pointer]
        self.pointer = self.pointer+1

        data = CsvToRatingAdapter(this_word)
        return data