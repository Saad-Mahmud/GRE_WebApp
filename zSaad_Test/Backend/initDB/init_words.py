from zSaad_Test.Backend.initDB.words import Words_Test, Words_Rating
import pandas as pd
import os
import random

word_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
word_dir = os.path.join(word_dir, 'Backend')
word_dir = os.path.join(word_dir, 'initDB')
Language_name = ['English','Bangali','Arabic','Chinese','French','German','Hindi','Italian','Japanese','Spanish']
encoding = "ISO-8859-1"

class CSVtoWord():

    def __init__(self,this_word,translation):
        wordID = "" + this_word["word"][0] + "_[" + this_word["word"] + "]"
        word = this_word["word"].strip()
        meanings = [this_word["meanings"].strip()]
        usages = [this_word["usages"].strip()]
        TYPE = this_word["TYPE"].strip()
        translations = {}
        for i in range(len(Language_name)):
            if (word != translation[Language_name[i]]):
                translations[Language_name[i]] = translation[Language_name[i]]
        self.wordObj = Words_Test(wordID=wordID, word=word, meanings=meanings, usages=usages, translations=translation,
                          TYPE=TYPE)


    def save(self):
        self.wordObj.save()


class DataLoader():

    def __init__(self):
        print(word_dir)
        self.df = pd.read_csv(word_dir+"/word_data.csv",sep='|')
        self.dftr = pd.read_csv(word_dir+"/transall.csv",sep='|')
        self.size=self.df.shape[0]
        print(self.size)
        self.pointer=0

    def re(self):
        self.pointer=0

    def hasNext(self):
        if(self.pointer>=self.size):return False
        return True

    def next_word(self):
        this_word=self.df.iloc[self.pointer]
        translation = self.dftr.iloc[self.pointer]
        self.pointer = self.pointer + 1
        data = CSVtoWord(this_word,translation)
        return data

    def next_ratings(self):
        aa=self.df.iloc[self.pointer]
        self.pointer=self.pointer+1
        wordID = ""+aa["word"][0]+"_["+aa["word"]+"]"
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


