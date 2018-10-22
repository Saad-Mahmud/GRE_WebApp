import operator

from zSaad_Test.Backend.initDB.words import Words_Rating, Words_Test


def fetch_easy_rating(country_id=0):
    print("I came in fetch_easy", Words_Rating.objects.__sizeof__())
    word_list = Words_Rating.objects()
    word_dict = {}
    for word in word_list:
        word_dict[word.wordID] = word.Ratings[country_id]
        #print("Titiiiiiiiiiiiiiiiiiiiiii : ", word.wordID, word.Ratings[0])
    sorted_dict = sorted(word_dict.items(), key=operator.itemgetter(1))

    for id, ratings in sorted_dict[1:5]:
        print("Now see if sort : ", id, ratings)
    #print("Hi there save me : ", sorted_dict[1:5])

    return sorted_dict[1:5]


def fetch_easy_words(country_id=0):
    final_easy_list = []
    rated_words = fetch_easy_rating(country_id)
    words_dict = Words_Test.objects()

    for w1 in rated_words:
        for w2 in words_dict:
            if w1[0] == w2.wordID:
                final_easy_list.append([w2.wordID, w2.word, w2.meanings, w2.usages, w2.translations, w2.TYPE ])

    for i in final_easy_list:
        print(i.wordID, i.word, i.meanings)
    print("helllooooooooooooooooo ", final_easy_list)

    return final_easy_list
