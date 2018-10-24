from random import randint

import operator
import random
import unicodedata

from flask import render_template, request, json

from zMA_Test.Backend.app import APP_MAIN
from zMA_Test.Backend.app.model import session_practice, session_test, user_word_history
from zMA_Test.Backend.practice.fetch_practice import fetch_easy_words, create_session_practice, \
    create_user_word_history, update_user_word_status
from zMA_Test.Backend.practice.practice_util import showstat
from zMA_Test.Backend.test.fetch_test import fetch_easy_words2, create_session_test


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/test')
def test():
    test_words = fetch_easy_words2()
    sessionID = create_session_test(test_words, 0)
    print("session mmm {}".format(sessionID.id))
    #option_words = fetch_easy_words2()
    #print(test_words[1][1])
    random_idx = random.sample(range(1, 10), 3)
    #print("rand idx", random_idx)
    option = []
    option.append(test_words[0][1])

    #print(option_words[9][1])
    for i in range(3):
        option.append(test_words[random_idx[i]][1])
    #print("options", option)

    random_idx2 = random.sample(range(1, 5), 4)
    #print(random_idx2)
    option_dict = {}
    for i in range(4):
        option_dict[unicodedata.normalize('NFKD', option[i]).encode('ascii','ignore')] = random_idx2[i]
    test_line =  unicodedata.normalize('NFKD', test_words[0][3][0]).encode('ascii','ignore')
    #print(type(test_line))
    #print("eeee", test_line)

    sorted_dict = sorted(option_dict.items(), key=operator.itemgetter(1))

    #print(type(sorted_dict))
    #print(sorted_dict)

    test_line = test_line.replace((unicodedata.normalize('NFKD', test_words[0][1]).encode('ascii','ignore')), "___")

    #print("eeeeeeeeeeeeeeeee", test_line)

    #print(type(option_dict))
    #print(option_dict)
    return render_template('test_new.html', test_word=test_words[0], test_line=test_line, option_dict=sorted_dict, sessionID=sessionID.id)

@APP_MAIN.route('/nexttestword', methods=['POST'])
def nextTestWord():
    answer = request.form['answer']
    sessionID = request.form['sessionID']
    pointer_f = session_test.objects(id=sessionID)[0]
    pointer = pointer_f.idx + 1
    test_words = pointer_f.words
    print('Ansssssssssssssss', answer)
    print('pointAnssssssssss', test_words[pointer_f.idx][1])
    pointer_f.idx = pointer
    pointer_f.save()
    test_word = test_words[pointer]
    return json.dumps({'test_word':test_word})


@APP_MAIN.route('/practice')
def practice():
    words = fetch_easy_words()
    status = {word['wordID']:'firstseen' for word in words}
    sessionID = create_session_practice(status, words, 0)
    #userWordHistory = create_user_word_history()

    return render_template('tryit.html', word=words[0], sessionID=sessionID.id)


@APP_MAIN.route('/fliped', methods=['POST'])
def translate():
    sessionID = request.form['sessionID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    pointer = pointer_f.idx # fetched pointer
    words = pointer_f.words # fetched word list

    if len(words)!=0:
        word = words[pointer]
    else:
        word = {'wordID':"$null$"}

    return json.dumps({'word': word})





@APP_MAIN.route('/nextword', methods=['POST'])
def nextWord():

    user_history = user_word_history.objects(username="moumita")[0]
    sessionID = request.form['sessionID']
    buttonID = request.form['buttonID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    pointer = pointer_f.idx # fetched, incremented pointer, saved the incremented pointer
    words = pointer_f.words
    oldStatus = pointer_f.status
    newStatus = oldStatus
    currentWord = words[pointer]
    currentWordID = currentWord['wordID']

    if buttonID=='ik':
        if newStatus[currentWordID]=='firstseen':
            newStatus[currentWordID] = 'yellow'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand, currentWord)

        elif newStatus[currentWordID]=='red':
            newStatus[currentWordID] = 'yellow'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand,currentWord)

        elif newStatus[currentWordID]=='yellow':
            newStatus[currentWordID] = 'green'
            words.remove(currentWord)

    elif buttonID=='idk':
        if newStatus[currentWordID]=='firstseen':
            newStatus[currentWordID] = 'red'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand, currentWord)

        elif newStatus[currentWordID]=='yellow':
            newStatus[currentWordID]='yellow'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand, currentWord)

    if len(words) != 0:
        pointer = (pointer + 1) % len(words)
        newWord = words[pointer]
        pointer_f.words = words
        pointer_f.status = newStatus
        pointer_f.idx = pointer
        pointer_f.save()
    else:
        pointer = -1
        newWord = {'wordID': '$null$'}


    print("word status ",  newStatus[currentWordID])
    user_history.status[currentWordID] = newStatus[currentWordID]
    user_history.save()
    mastered, reviewing, learning = showstat(newStatus)

    return json.dumps({'word': newWord, 'learning': learning, 'reviewing':reviewing, 'mastered':mastered})

@APP_MAIN.route('/tryit')
def tryit():
    return render_template('moumitadummy.html')