import json
from random import randint

from flask import render_template, request, redirect, url_for, send_from_directory
from flask_login import login_required, current_user

from App_Main.Backend.App import APP_MAIN
from App_Main.Backend.Words.Words import Words
from zMA_Test.Backend.app.model import session_practice, user_word_history, review_words
from zMA_Test.Backend.practice.builderpattern import ConcreteBuilderPracticeSummary, DirectorPracticeSummary
from zMA_Test.Backend.practice.builderpattern2 import ConcreteBuilderNextWord, DirectorNextWord
from zMA_Test.Backend.practice.fetch_practice import FetchWords, create_session_practice, update_review_words, \
    fetch_session_practice, fetch_user_word_history, fetch_review_words
from zMA_Test.Backend.practice.memento_pattern import Caretaker, Originator
from zMA_Test.Backend.practice.practice_util import showstat


@APP_MAIN.route('/practice')
@login_required
def practice_intro():
    if current_user.is_authenticated:
        return render_template("practice.html")
    return redirect(url_for("hello_world"))


@APP_MAIN.route('/practice/<type>')
@login_required
def practice(type):
    if current_user.is_authenticated:
        fetchwords = FetchWords(current_user.username)
        words = fetchwords.practice_words(type,"practice")
        status = {word['wordID']:'firstseen' for word in words}
        sessionID = create_session_practice(status, words, 0, words)

        return render_template('practicedummy.html', word=words[0], sessionID=sessionID.id, length=len(words))
    else:
        return redirect(url_for("hello_world"))


@APP_MAIN.route('/fliped', methods=['POST'])
@login_required
def flip():
    sessionID = request.form['sessionID']
    pointer_f = fetch_session_practice(sessionID)

    pointer = pointer_f.idx
    words = pointer_f.edited_words

    if len(words)!=0:
        word = words[pointer]
    else:
        word = {'wordID':"$null$"}

    return json.dumps({'word': word})


@APP_MAIN.route('/nextword', methods=['POST'])
@login_required
def nextWord():
    user_history = fetch_user_word_history(current_user.username)
    sessionID = request.form['sessionID']
    buttonID = request.form['buttonID']
    pointer_f = fetch_session_practice(sessionID)

    # .....................................Builder pattern is used to produce next word...........................................
    concrete_builder_next_word = ConcreteBuilderNextWord()
    director_next_word = DirectorNextWord(pointer_f, buttonID, user_history)
    director_next_word.constructNextWord(concrete_builder_next_word)
    next_word_obj = concrete_builder_next_word.next_word_object

    return json.dumps(
        {'word': next_word_obj.newWord, 'learning': next_word_obj.learning, 'reviewing': next_word_obj.reviewing,
         'mastered': next_word_obj.mastered})


@APP_MAIN.route('/practicesummary', methods=['POST'])
@login_required
def practice_summary():
    sessionID = request.form['sessionID']
    pointer_f = fetch_session_practice(sessionID)

    # .....................................Builder pattern is used to create summary...........................................

    concrete_practice_builder = ConcreteBuilderPracticeSummary()
    director_practice = DirectorPracticeSummary(pointer_f)
    director_practice.constructPracticeSummary(concrete_practice_builder)
    practice_sum = concrete_practice_builder.practice_summary_object

    # .....................................Memento pattern is used to save the summary...........................................
    prev_sum = update_review_words(current_user.username, pointer_f.words)

    caretaker = Caretaker()
    originator = Originator()
    originator.setState(prev_sum)
    caretaker.addMemento(originator.save())

    return render_template('practicesummary.html', words=practice_sum.practice_words, correct=practice_sum.correct,
                           wrong=practice_sum.wrong)


@APP_MAIN.route('/previouspractice')
@login_required
def previous_practice():
    # .......................................Memento Pattern is used to restore the summary......................................
    caretaker = Caretaker()
    originator = Originator()

    #If you want to show all review words #
    summaries_obj = fetch_review_words(current_user.username)
    summaries = summaries_obj.summary
    for sum in summaries:
        originator.setState(sum)
        caretaker.addMemento(originator.save())
    #.......................................#

    if caretaker.mementos.__len__() > 0:
        last_sum = originator.restore(caretaker.getMemento((caretaker.mementos.__len__() - 1)))
        return render_template("practice_prev_summary.html", words=last_sum)
    else:
        return render_template("practice_no_summary.html")

@APP_MAIN.route('/specificpractice', methods=['POST'])
@login_required
def specific_practice():

    sumpath = request.form['practicesum']
#............................................Memento is used to restore a defined summary....................................
    caretaker = Caretaker()
    originator = Originator()

    # If you want to show all review words #
    summaries_obj = fetch_review_words(current_user.username)
    summaries = summaries_obj.summary
    for sum in summaries:
        originator.setState(sum)
        caretaker.addMemento(originator.save())

    #.......................................#

    if int(sumpath) > caretaker.mementos.__len__():
        return render_template("practice_no_summary.html")
    else:
        last_sum = originator.restore(caretaker.getMemento(int(sumpath)-1))
        return render_template("practice_prev_summary.html", words=last_sum, mem_len=caretaker.mementos.__len__())



