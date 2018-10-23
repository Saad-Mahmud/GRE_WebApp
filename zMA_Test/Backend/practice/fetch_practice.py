import operator

from zMA_Test.Backend.app.model import session_practice
from zSaad_Test.Backend.initDB.words import Words_Rating, Words_Test

def takeSecond(elem, country_id):
    return elem[1][country_id]
def fetch_easy_rating(country_id=0):
    #print("I came in fetch_easy", Words_Rating.objects.__sizeof__())

    """

    :param country_id:
    :return:


    temp_list = Words_Test.objects()

    temps = [
        {
            'wordID': w.wordID,
            'word': w.word,
            'TYPE': w.TYPE,
            'meaning': w.meanings[0],
            'usages': w.usages
        }
        for w in temp_list
    ]
    for w in temps:
        print("words ",w['wordID'])
    """

    temp_list = Words_Rating.objects()

    temps = [
        {
            'wordID': w.wordID,
            'Ratings': w.Ratings,

        }
        for w in temp_list
    ]


    sorted_temp = sorted(temps, key=lambda k: k['Ratings'][country_id])
    """
    for w in sorted_temp:
        print("words ", w['wordID'], w['Ratings'][country_id])
    
    word_list = Words_Rating.objects()
    word_dict = {}
    
    for word in word_list:
        word_dict[word.wordID] = word.Ratings[country_id]
        
        #print("Titiiiiiiiiiiiiiiiiiiiiii : ", word.wordID, word.Ratings[0])
    sorted_dict = sorted(word_dict.items(), key=operator.itemgetter(1))

    
    for id, ratings in sorted_dict[1:5]:
        print("Now see if sort : ", id, ratings)
    #print("Hi there save me : ", sorted_dict[1:5])
    """

    return sorted_temp[1:5]


def fetch_easy_words(country_id=0):

    final_list = []
    rated_words = fetch_easy_rating(country_id)
    words_dict = Words_Test.objects()

    for w1 in rated_words:
        for w2 in words_dict:
            if w1['wordID'] == w2.wordID:
                print("meaningggggg : ", w2.word, w2.meanings)
                #final_easy_list.append([w2.wordID, w2.word, w2.meanings, w2.usages, w2.translations, w2.TYPE ])
                final_list.append(
                    {
                        'wordID': w2.wordID,
                        'word': w2.word,
                        'TYPE': w2.TYPE,
                        'meaning': w2.meanings[0],
                        'usages': w2.usages
                    })

    """
        for i in final_list:
        print("final list ",i['wordID'], i['word'], i['meaning'])
    """


    return final_list


def create_session_practice(status,words,idx):
    session= session_practice(status=status, words=words, idx=idx)
    session2 = session.save()
    return session2
