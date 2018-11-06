from zSaad_Test.Backend.words.WordDataLoader import WordDataLoader
from zSaad_Test.Backend.words.WordRatingLoader import WordRatingLoader
from zSaad_Test.Backend.initDB import initDB_Config as Conf


def init_DB_with_words():

    try:
        dataloader = WordDataLoader(Conf.initDB_dir + "/word_data.csv", Conf.initDB_dir + "/transall.csv")
    except IOError as error:
        print('Caught this error: ' + repr(error))
        dataloader = None

    if(dataloader is not None):
        while(dataloader.hasNext()):
            try:
                dataloader.next_word().save()
            except IndexError as error:
                print('Caught this error: ' + repr(error))
    else:
        return


    try:
        dataloader = WordRatingLoader(Conf.initDB_dir + "/word_data.csv")
    except IOError as error:
        print('Caught this error: ' + repr(error))
        dataloader = None

    if (dataloader is not None):
        while (dataloader.hasNext()):
            try:
                dataloader.next_ratings().save()
            except IndexError as error:
                print('Caught this error: ' + repr(error))
                break



