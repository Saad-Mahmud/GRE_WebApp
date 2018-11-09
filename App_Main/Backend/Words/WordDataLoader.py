import pandas as pd

from App_Main.Backend.Words.CsvToWordAdapter import CsvToWordAdapter


class WordDataLoader():

    def __init__(self,word_path,trans_path):
        try:
            self.df = pd.read_csv(word_path,sep='|')
            if (trans_path is not None):
                self.dftr = pd.read_csv(trans_path,sep='|')
                self.lang = list(self.dftr)
                #print (self.lang)
            else:
                self.dftr = None
                self.lang = None
        except IOError as error:
            print (error)
            raise IOError

        self.size=self.df.shape[0]
        self.pointer=0

    def hasNext(self):
        if(self.pointer>=self.size):return False
        return True

    def next_word(self):
        if(self.pointer>=self.size):
            raise IndexError

        this_word=self.df.iloc[self.pointer]

        if(self.dftr is not None):
            translation = self.dftr.iloc[self.pointer]
        else:
            translation = None

        self.pointer = self.pointer + 1
        data = CsvToWordAdapter(this_word, translation,self.lang)
        return data