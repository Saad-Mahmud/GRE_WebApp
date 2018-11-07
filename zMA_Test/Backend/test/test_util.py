from zSaad_Test.Backend.words.Words_Rating import Words_Rating


def show_test_stat(status):
    correct = 0
    wrong = 0

    for s in status.items():
        if s[1] == s[0]:
            correct += 1
        else:
            wrong += 1
    return correct, wrong


def rating_change(status, words):

    i = 0
    for s in status.items():
        rat_obj = Words_Rating.objects(wordID = words[i][0])[0]
        if s[1] == s[0]:

            rat_obj.Ratings[0] = rat_obj.Ratings[0] - 1
            """
            for p in rat_obj:
                if p.wordID == words[i][0]:
                    print("ageeeeeeeeeee ", p.wordID, p.Ratings[0])
                    p.Ratings[0] = p.Ratings[0] - 1
                    print("poreeeeeeeeee ", p.wordID, p.Ratings[0])
                    """
        else:
            rat_obj.Ratings[0] = rat_obj.Ratings[0] + 1

            # for p in rat_obj:
            #     if p.wordID == words[i][0]:
            #         p.Ratings[0] = p.Ratings[0] + 1
        i += 1
        rat_obj.save()
    #rat_obj.update()