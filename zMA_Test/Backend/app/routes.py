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
    sessionID = create_session_practice(words,0)
    print("session mmm {}".format(sessionID.id))
    print("status ", words[0]);

    return render_template('tryit.html', word=words[0], sessionID=sessionID.id)


@APP_MAIN.route('/test')
def test():
    return render_template('test.html')

@APP_MAIN.route('/clicked', methods=['POST'])
def translate():
    sessionID = request.form['sessionID']
    pointer_f = session_practice.objects(id=sessionID)[0]
    pointer = pointer_f.idx
    words = pointer_f.words

    print("pointer: " + str(pointer))
    word = words[pointer]

    return json.dumps({'word': word})

@APP_MAIN.route('/nextword', methods=['POST'])
def nextWord():
    sessionID = request.form['sessionID']
    pointer_f = session_practice.objects(id=sessionID)[0]
    pointer = pointer_f.idx + 1
    words = pointer_f.words
    pointer_f.idx = pointer
    pointer_f.save()
    print("pointer: " + str(pointer))
    word = words[pointer]

    return json.dumps({'word': word})

@APP_MAIN.route('/tryit')
def tryit():
    return render_template('tryit.html')