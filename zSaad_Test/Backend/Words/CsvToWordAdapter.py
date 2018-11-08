from zSaad_Test.Backend.Words.Words import Words


class CsvToWordAdapter():

    def __init__(self,this_word,translation,lang):

        wordID = "" + this_word["word"][0] + "_[" + this_word["word"] + "]"
        word = this_word["word"].strip()
        meanings = [this_word["meanings"].strip()]
        usages = [this_word["usages"].strip()]
        TYPE = this_word["TYPE"].strip()
        translations = {}

        if(translations is not None and lang is not None):
            for i in range(len(lang)):
                if (word != translation[lang[i]]):
                    translations[lang[i]] = translation[lang[i]]

        self.wordObj = Words(wordID=wordID, word=word, meanings=meanings,
                        usages=usages, translations=translation, TYPE=TYPE)


    def save(self):
        self.wordObj.save()


