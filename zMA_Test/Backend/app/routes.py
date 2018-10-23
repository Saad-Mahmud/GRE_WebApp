from random import randint

from zMA_Test.Backend.app import APP_MAIN
from flask import render_template, redirect,url_for,flash,send_file,request,json

from zMA_Test.Backend.app.model import session_practice
from zMA_Test.Backend.practice.fetch_practice import fetch_easy_words, create_session_practice


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/practice')
def practice():
    words = fetch_easy_words()
    status = {word['wordID']:'red' for word in words}
    sessionID = create_session_practice(status, words, 0)

    return render_template('tryit.html', word=words[0], sessionID=sessionID.id)


@APP_MAIN.route('/test')
def test():
    return render_template('test.html')


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
    sessionID = request.form['sessionID']
    buttonID = request.form['buttonID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    pointer = pointer_f.idx # fetched, incremented pointer, saved the incremented pointer
    words = pointer_f.words
    status = pointer_f.status
    currentWord = words[pointer]
    currentWordID = currentWord['wordID']

    if buttonID=='ik':
        if status[currentWordID]=='red':
            status[currentWordID] = 'yellow'

            words.remove(currentWord)
            rand = randint(0, len(words))
            # print("randint ", rand)
            words.insert(rand,currentWord)

        elif status[currentWordID]=='yellow':
            status[currentWordID] = 'green'
            words.remove(currentWord)

    elif buttonID=='idk':
        if status[currentWordID]=='yellow':
            status[currentWordID]='yellow'

            words.remove(currentWord)
            rand = randint(0, len(words))
            # print("blaint ", rand)
            words.insert(rand, currentWord)

    if len(words) != 0:
        pointer = (pointer + 1) % len(words)
        newWord = words[pointer]
        pointer_f.words = words
        pointer_f.status = status
        pointer_f.idx = pointer
        pointer_f.save()
    else:
        pointer = -1
        newWord = {'wordID': '$null$'}

    return json.dumps({'word': newWord})

@APP_MAIN.route('/tryit')
def tryit():
    return render_template('tryit.html')