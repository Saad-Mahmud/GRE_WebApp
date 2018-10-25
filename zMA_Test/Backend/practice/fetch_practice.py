import operator

from zMA_Test.Backend.app.model import session_practice, user_word_history
from zSaad_Test.Backend.initDB.words import Words_Rating, Words_Test


def fetch_easy_rating(country_id=0):
    # print("I came in fetch_easy", Words_Rating.objects.__sizeof__())

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

    already_seen_words = user_word_history.objects(username="moumita")[0]
    temp_list = Words_Rating.objects()

    temps = [
        {
            'wordID': w.wordID,
            'Ratings': w.Ratings,

        }
        for w in temp_list
    ]

    sorted_temp = sorted(temps, key=lambda k: k['Ratings'][country_id])
    new_list = []

    for i in range(0, 333):
        if sorted_temp[i]['wordID'] not in already_seen_words.status:
            print("bla ")
            new_list.append(sorted_temp[i])

        else:
            if already_seen_words.status[sorted_temp[i]['wordID']]!='green':
                new_list.append(sorted_temp[i])
                print("maf chai ", sorted_temp[i]['wordID'])



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
    if len(new_list)>=10:
        return new_list[0:10]
    else:
        sorted_temp[0:10]


def fetch_easy_words(country_id=0):
    final_list = []
    rated_words = fetch_easy_rating(country_id)
    words_dict = Words_Test.objects()

    for w1 in rated_words:
        for w2 in words_dict:
            if w1['wordID'] == w2.wordID:
                print("meaningggggg : ", w2.word, w2.meanings)
                # final_easy_list.append([w2.wordID, w2.word, w2.meanings, w2.usages, w2.translations, w2.TYPE ])
                final_list.append(
                    {
                        'wordID': w2.wordID,
                        'word': w2.word,
                        'TYPE': w2.TYPE,
                        'meaning': w2.meanings[0],
                        'usage': w2.usages[0],
                        'translations': w2.translations
                    })

    """
        for i in final_list:
        print("final list ",i['wordID'], i['word'], i['meaning'])
    """

    return final_list


def create_session_practice(status, words, idx):
    session = session_practice(status=status, words=words, idx=idx)
    session2 = session.save()
    return session2


def create_user_word_history():
    wordHistory = user_word_history("moumita")
    wordHistory2 = wordHistory.save()
    return wordHistory2


def update_user_word_status(oldStatus, newStatus):
    mergedList = newStatus + [s for s in oldStatus if s not in oldStatus]
    return mergedList
