import operator
import random
import unicodedata
from random import randint

from flask import render_template, request, json, send_file

from zMA_Test.Backend.app import APP_MAIN
from zMA_Test.Backend.app.model import session_practice, session_test, user_word_history, Gre_data
from zMA_Test.Backend.practice.fetch_practice import fetch_easy_words, create_session_practice
from zMA_Test.Backend.practice.practice_util import showstat
from zMA_Test.Backend.test.fetch_test import fetch_easy_words2, create_session_test
from zMA_Test.Backend.test.test_util import show_test_stat
from zSaad_Test.Backend.initDB.words import Words_Test


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")



@APP_MAIN.route('/test')
def test():
    #username = unicodedata.normalize('NFKD', current_user.username).encode('ascii', 'ignore')
    #print(type(username))
    test_words = fetch_easy_words2()
    status = {}
    ques_multi = []
    ques_blank = []
    #sessionID = create_session_test(status, test_words, 0, questions)
    temp = Gre_data.objects(username="amit99")[0]

    #print("session mmm {}".format(sessionID.id))
    print(type(test_words))
    random_idx = random.sample(range(1, 10), 3)
    option = []
    option_multiple_choice = []

    option.append(test_words[0][1])
    option_multiple_choice.append(test_words[0][2][0])
    print('amiiiiiiii', test_words[0][2][0])

    # print("aaaaaaaaaaaaaa", type(test_words[0][1]))
    for i in range(3):
        option.append(test_words[random_idx[i]][1])
        option_multiple_choice.append(test_words[random_idx[i]][2][0])

    random_idx2 = random.sample(range(1, 5), 4)
    option_dict = {}
    option_multiple_choice_dict = {}

    for i in range(4):
        option_dict[unicodedata.normalize('NFKD', option[i]).encode('ascii', 'ignore')] = random_idx2[i]
        option_multiple_choice_dict[
            unicodedata.normalize('NFKD', option_multiple_choice[i]).encode('ascii', 'ignore')] = random_idx2[i]

    test_multi_choice_word = ''
    test_line = unicodedata.normalize('NFKD', test_words[0][3][0]).encode('ascii', 'ignore')
    test_multi_choice_word += 'Meaning of '
    choice_word = unicodedata.normalize('NFKD', test_words[0][1]).encode('ascii', 'ignore')
    choice_word = choice_word.upper()
    test_multi_choice_word += choice_word

    print('multichoice', test_multi_choice_word)
    print(type(test_multi_choice_word))

    sorted_dict = sorted(option_dict.items(), key=operator.itemgetter(1))
    sorted_multi_choice_dict = sorted(option_multiple_choice_dict.items(), key=operator.itemgetter(1))

    print('#######################')
    print(type(sorted_multi_choice_dict))
    print(type(sorted_dict))
    print('#######################')

    test_line = test_line.replace((unicodedata.normalize('NFKD', test_words[0][1]).encode('ascii', 'ignore')), "___")

    ans_blanks = unicodedata.normalize('NFKD', test_words[0][1]).encode('ascii', 'ignore')
    ans_multi = unicodedata.normalize('NFKD', test_words[0][2][0]).encode('ascii', 'ignore')

    print(ans_multi)
    ques_multi.append(test_multi_choice_word)
    ques_blank.append(test_line)
    sessionID = create_session_test(status, test_words, 0, ques_multi, ques_blank)


    return render_template('test_new.html', test_word=test_words[0], test_line=test_line,
                           multi_word=test_multi_choice_word, option_dict=sorted_dict,
                           multi_dict=sorted_multi_choice_dict, sessionID=sessionID.id)


@APP_MAIN.route('/nexttestword', methods=['POST'])
def nextTestWord():
    #username = unicodedata.normalize('NFKD', current_user.username).encode('ascii', 'ignore')
    username = 'amit99'
    answer = request.form['answer']
    sessionID = request.form['sessionID']
    isWhat = request.form['isWhat']

    isWhat = unicodedata.normalize('NFKD', isWhat).encode('ascii', 'ignore')
    print("pppppppppppppp", type(isWhat))
    pointer_f = session_test.objects(id=sessionID)[0]
    pointer = pointer_f.idx + 1
    test_words = pointer_f.words

    if isWhat == 'true':
        pointer_f.status[test_words[pointer_f.idx][1]] = answer
        print('GivenAnsssssssssssssss1', answer)
        print('ActualAnssssssssssssss1', test_words[pointer_f.idx][1])
    else:
        pointer_f.status[test_words[pointer_f.idx][2][0]] = answer
        print('GivenAnsssssssssssssss2', answer)
        print('ActualAnssssssssssssss2', test_words[pointer_f.idx][2][0])

    pointer_f.idx = pointer
    pointer_f.save()

    if pointer < len(test_words):
        test_word = test_words[pointer]
        option = []

        if isWhat == 'true':
            option.append(test_word[1])
        else:
            option.append(test_word[2][0])

        if pointer <= 3:
            random_idx1 = random.sample(range(0, pointer), 1)
            random_idx2 = random.sample(range(pointer + 1, 10), 2)
            random_idx = random_idx1 + random_idx2
        elif pointer <= 7:
            random_idx1 = random.sample(range(0, pointer), 2)
            random_idx2 = random.sample(range(pointer + 1, 10), 1)
            random_idx = random_idx1 + random_idx2
        else:
            random_idx = random.sample(range(0, pointer), 3)

        for i in range(3):
            if isWhat == 'true':
                option.append(test_words[random_idx[i]][1])
            else:
                option.append(test_words[random_idx[i]][2][0])

        random_idx_option = random.sample(range(1, 5), 4)
        option_dict = {}

        for i in range(4):
            option_dict[unicodedata.normalize('NFKD', option[i]).encode('ascii', 'ignore')] = random_idx_option[i]

        sorted_dict = sorted(option_dict.items(), key=operator.itemgetter(1))
        correct, wrong = show_test_stat(pointer_f.status)
        if isWhat == 'true':
            test_line = unicodedata.normalize('NFKD', test_word[3][0]).encode('ascii', 'ignore')
            test_line = test_line.replace((unicodedata.normalize('NFKD', test_word[1]).encode('ascii', 'ignore')),
                                          "___")
            pointer_f.ques_blank.append(test_line)
            pointer_f.save()
            return json.dumps({'test_word': test_word, 'test_line': test_line, 'option_dict': sorted_dict, 'correct': correct, 'wrong': wrong})
        else:
            test_multi_choice_word = ''
            test_multi_choice_word += 'Meaning of '
            choice_word = unicodedata.normalize('NFKD', test_word[1]).encode('ascii', 'ignore')
            choice_word = choice_word.upper()
            test_multi_choice_word += choice_word
            pointer_f.ques_multi.append(test_multi_choice_word)
            pointer_f.save()
            return json.dumps({'test_word': test_word, 'test_line': test_multi_choice_word, 'option_dict': sorted_dict, 'correct': correct, 'wrong': wrong})

    else:
        test_word = ['$null$']
        session_data = session_test.objects(id=sessionID)[0]
        print("abcdefgh", session_data.status)
        test_key = 'test' + sessionID
        gre_test_words = {
            test_key: session_data.status
        }

        print("==================================")
        correct, wrong = show_test_stat(pointer_f.status)
        print(correct, wrong)

        gre_data = Gre_data.objects(username=username)[0]
        print(gre_data.username)
        gre_data.history[test_key] = session_data.status
        gre_data.save()

        print("Ppppppppppppppppppppp", gre_test_words)
        return json.dumps({'test_word': test_word, 'correct': correct, 'wrong': wrong})


@APP_MAIN.route('/thisans', methods=['POST'])
def nextAns():
    sessionID = request.form['sessionID']
    isWhat = request.form['isWhat']
    isWhat = unicodedata.normalize('NFKD', isWhat).encode('ascii', 'ignore')

    pointer_f = session_test.objects(id=sessionID)[0]
    test_words = pointer_f.words


    if isWhat == 'true':
        answer = test_words[pointer_f.idx][1]
    else:
        answer = test_words[pointer_f.idx][2][0]

    return json.dumps({'ans': answer})

@APP_MAIN.route('/testsummary', methods=['POST'])
def summary():
    sessionID = request.form['sessionID']
    print(sessionID)
    isWhat = request.form['isWhat']
    print(isWhat)
    correct = request.form['correct']
    print(correct)
    wrong = request.form['wrong']
    print(wrong)

    pointer_f = session_test.objects(id=sessionID)[0]
    test_words = pointer_f.words

    if isWhat=='true':
        ques = pointer_f.ques_blank
    else:
        ques = pointer_f.ques_multi

    status = pointer_f.status
    correct_ans=[]
    your_ans=[]

    for the_key, the_value in status.iteritems():
        correct_ans.append(the_key)
        your_ans.append(the_value)

    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    print(correct_ans)
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(your_ans)

    print(test_words)

    return render_template("test_summary.html", correct=correct, wrong=wrong, isWhat=isWhat,
                           test_words=test_words, ques=ques, correct_ans=correct_ans, your_ans=your_ans)


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

import os
static_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
static_dir = os.path.join(static_dir, 'Frontend')
static_dir = os.path.join(static_dir, 'static')
static_dir = os.path.join(static_dir, 'audio')

@APP_MAIN.route('/words/audio/',defaults={'filename': ''})
@APP_MAIN.route('/words/audio/<path:filename>')
def download_file(filename):
    file = ''
    for i in range(len(filename)-4):
        file =file+filename[i]
    print(file)
    filename = os.path.join(static_dir, filename)
    if(Words_Test.objects(word=file)==[]):
        return
    return send_file(filename)
