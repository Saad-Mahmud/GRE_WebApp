from App_Main.Backend.Words.WordDataLoader import WordDataLoader
from App_Main.Backend.Words.WordRatingLoader import WordRatingLoader
from App_Main.Backend.Config.DBConfig import DBConf


def init_DB_with_words():

    Conf = DBConf.getInstance()

    try:
        dataloader = WordDataLoader(Conf.initDB_dir + "/word_data.csv", Conf.initDB_dir + "/transall.csv")
    except IOError as error:
        print('Caught this error1: ' + repr(error))
        dataloader = None

    if(dataloader is not None):
        while(dataloader.hasNext()):
            try:
                dataloader.next_word().save()
            except IndexError as error:
                print('Caught this error2: ' + repr(error))
    else:
        return


    try:
        dataloader = WordRatingLoader(Conf.initDB_dir + "/word_data.csv")
    except IOError as error:
        print('Caught this error11: ' + repr(error))
        dataloader = None

    if (dataloader is not None):
        while (dataloader.hasNext()):
            try:
                dataloader.next_ratings().save()
            except IndexError as error:
                print('Caught this error22: ' + repr(error))
                break



def AddDataToDB(name):

    Conf = DBConf.getInstance()

    try:
        dataloader = WordDataLoader(Conf.initDB_dir + "/"+name+".csv", None)
    except IOError as error:
        print('Caught this error3: ' + repr(error))
        dataloader = None

    if(dataloader is not None):
        while(dataloader.hasNext()):
            try:
                dataloader.next_word().save()
            except IndexError as error:
                print('Caught this error4: ' + repr(error))
    else:
        return


    try:
        dataloader = WordRatingLoader(Conf.initDB_dir + "/"+name+".csv")
    except IOError as error:
        print('Caught this error5: ' + repr(error))
        dataloader = None

    if (dataloader is not None):
        while (dataloader.hasNext()):
            try:
                dataloader.next_ratings().save()
            except IndexError as error:
                print('Caught this error: ' + repr(error))
                break



