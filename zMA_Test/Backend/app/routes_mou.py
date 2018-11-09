import json
from random import randint

from flask import render_template, request
from flask_login import login_required, current_user

from App_Main.Backend.App import APP_MAIN
from zMA_Test.Backend.app.model import session_practice, user_word_history
from zMA_Test.Backend.practice.builderpattern import ConcreteBuilderPracticeSummary, DirectorPracticeSummary
from zMA_Test.Backend.practice.fetch_practice import FetchWords, create_session_practice
from zMA_Test.Backend.practice.practice_util import showstat


@login_required
@APP_MAIN.route('/practice')
def practice_intro():
    return render_template("practice.html")


@APP_MAIN.route('/practice/<type>')
def practice(type):
    print("type ", type)
    fetchwords = FetchWords(current_user.username)
    words = fetchwords.practice_words(type,"practice")
    status = {word['wordID']:'firstseen' for word in words}

    sessionID = create_session_practice(status, words, 0, words)
    #userWordHistory = create_user_word_history()

    return render_template('practicedummy.html', word=words[0], sessionID=sessionID.id)


@APP_MAIN.route('/fliped', methods=['POST'])
def translate_ma():
    sessionID = request.form['sessionID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    pointer = pointer_f.idx # fetched pointer
    words = pointer_f.edited_words # fetched word list

    if len(words)!=0:
        word = words[pointer]
    else:
        word = {'wordID':"$null$"}

    return json.dumps({'word': word})


@APP_MAIN.route('/nextword', methods=['POST'])
def nextWord():

    #user_history = user_word_history.objects(username="moumita")[0]
    user_history = user_word_history.objects(username=current_user.username)[0]
    sessionID = request.form['sessionID']
    buttonID = request.form['buttonID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    pointer = pointer_f.idx # fetched, incremented pointer, saved the incremented pointer
    words = pointer_f.edited_words
    oldStatus = pointer_f.status
    newStatus = oldStatus
    currentWord = words[pointer]
    currentWordID = currentWord['wordID']
    history = pointer_f.history

    if currentWordID not in history:
        history[currentWordID] = {buttonID}
    else:
        history[currentWordID].append(buttonID)

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
        pointer_f.edited_words = words
        pointer_f.status = newStatus
        pointer_f.idx = pointer
        pointer_f.history = history
        pointer_f.save()
    else:
        pointer = -1
        newWord = {'wordID': '$null$'}
        pointer_f.history = history
        pointer_f.save()


    print("word status ",  newStatus[currentWordID])
    user_history.status[currentWordID] = newStatus[currentWordID]
    user_history.save()
    mastered, reviewing, learning = showstat(newStatus)

    return json.dumps({'word': newWord, 'learning': learning, 'reviewing':reviewing, 'mastered':mastered})


@APP_MAIN.route('/practicesummary', methods=['POST'])
def practice_summary():
    sessionID = request.form['sessionID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    concrete_practice_builder = ConcreteBuilderPracticeSummary()
    director_practice = DirectorPracticeSummary(pointer_f)
    director_practice.constructPracticeSummary(concrete_practice_builder)
    practice_sum = concrete_practice_builder.practice_summary_object

    #
    #
    # words = pointer_f.words
    # history = pointer_f.history
    # correct, wrong = create_summary(words,history)
    #
    # for key,v in correct.items():
    #     print("corrrect ", key, v)
    # return render_template('practicesummary.html', words=words, correct=correct, wrong=wrong )
    return render_template('practicesummary.html', words=practice_sum.practice_words, correct=practice_sum.correct,
                           wrong=practice_sum.wrong)


@APP_MAIN.route('/tryit')
def tryit():
    return render_template('practicedummy.html')