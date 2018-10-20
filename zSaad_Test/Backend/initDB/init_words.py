from zSaad_Test.Backend.initDB.words import Words_Test,Words_Rating
import pandas as pd
import os
import random

word_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
word_dir = os.path.join(word_dir, 'Backend')
word_dir = os.path.join(word_dir, 'initDB')
encoding = "ISO-8859-1"

class DataLoader():

    def __init__(self):
        print(word_dir)
        self.df = pd.read_csv(word_dir+"/word_data.csv")
        self.size=self.df.shape[0]
        print(self.size)
        self.pointer=0

    def re(self):
        self.pointer=0

    def hasNext(self):
        if(self.pointer>=self.size):return False
        return True

    def next_word(self):
        aa=self.df.iloc[self.pointer]
        self.pointer=self.pointer+1
        wordID = "A_["+aa["word"].strip()+"]_MAIN"
        word = aa["word"].strip()
        meanings = [aa["meanings"].strip()]
        usages = [aa["usages"].strip()]
        TYPE = aa["TYPE"].strip()
        translation = {}
        return Words_Test(wordID=wordID,word=word,meanings=meanings,usages=usages,translations=translation,TYPE=TYPE)

    def next_ratings(self):
        aa=self.df.iloc[self.pointer]
        self.pointer=self.pointer+1
        wordID = "A_["+aa["word"].strip()+"]_MAIN"
        ratings = [1+random.randint(1,10)%10 for i in range(200)]
        return Words_Rating(wordID=wordID,Ratings=ratings)


def init_DB_with_words():

    print("here")
    dataloader = DataLoader()
    while(dataloader.hasNext()):
        data = dataloader.next_word().save()
    dataloader.re()
    while(dataloader.hasNext()):
        data = dataloader.next_ratings().save()
    return


