import json
from random import randint

from flask import render_template, request, redirect, url_for, send_from_directory
from flask_login import login_required, current_user

from App_Main.Backend.App import APP_MAIN
from App_Main.Backend.Words.Words import Words
from zMA_Test.Backend.app.model import session_practice, user_word_history, review_words
from zMA_Test.Backend.practice.builderpattern import ConcreteBuilderPracticeSummary, DirectorPracticeSummary
from zMA_Test.Backend.practice.builderpattern2 import ConcreteBuilderNextWord, DirectorNextWord
from zMA_Test.Backend.practice.fetch_practice import FetchWords, create_session_practice, update_review_words
from zMA_Test.Backend.practice.memento_pattern import Caretaker, Originator
from zMA_Test.Backend.practice.practice_util import showstat




@APP_MAIN.route('/practice')
@login_required
def practice_intro():
    if current_user.is_authenticated:
        return render_template("practice.html")
    return redirect(url_for("hello_world"))

@login_required
@APP_MAIN.route('/practice/<type>')
def practice(type):
    if current_user.is_authenticated:
        fetchwords = FetchWords(current_user.username)
        words = fetchwords.practice_words(type,"practice")
        status = {word['wordID']:'firstseen' for word in words}
        sessionID = create_session_practice(status, words, 0, words)
        #userWordHistory = create_user_word_history()
        return render_template('practicedummy.html', word=words[0], sessionID=sessionID.id)
    else:
        return redirect(url_for("hello_world"))


@APP_MAIN.route('/fliped', methods=['POST'])
@login_required
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

@login_required
@APP_MAIN.route('/nextword', methods=['POST'])
def nextWord():
    user_history = user_word_history.objects(username=current_user.username)[0]
    sessionID = request.form['sessionID']
    buttonID = request.form['buttonID']
    pointer_f = session_practice.objects(id=sessionID)[0]

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
    pointer_f = session_practice.objects(id=sessionID)[0]

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


@APP_MAIN.route('/previouspractice')
@login_required
def previous_practice():
    # .......................................Memento Pattern is used to restore the summary......................................
    caretaker = Caretaker()
    originator = Originator()

    #If you want to show all review words #
    summaries_obj = review_words.objects(username=current_user.username)[0]
    summaries = summaries_obj.summary
    for sum in summaries:
        originator.setState(sum)
        caretaker.addMemento(originator.save())
    #.......................................#


    if caretaker.mementos.__len__() > 0:
        last_sum = originator.restore(caretaker.getMemento((caretaker.mementos.__len__() - 1)))
        for l in last_sum:
            print("laassssssssssst ", l)
        return render_template("practice_prev_summary.html", words=last_sum)
    else:
        return render_template("test_no_summary.html")

@APP_MAIN.route('/specificpractice', methods=['POST'])
@login_required
def specific_practice():

    sumpath = request.form['practicesum']
#............................................Memento is used to restore a defined summary....................................
    caretaker = Caretaker()
    originator = Originator()

    # If you want to show all review words #
    summaries_obj = review_words.objects(username=current_user.username)[0]
    summaries = summaries_obj.summary
    for sum in summaries:
        originator.setState(sum)
        caretaker.addMemento(originator.save())

    #.......................................#

    if int(sumpath) > caretaker.mementos.__len__():
        return render_template("test_no_summary.html")
    else:
        last_sum = originator.restore(caretaker.getMemento(int(sumpath)-1))
        for l in last_sum:
            print("laassssssssssst ", l)
        return render_template("practice_prev_summary.html", words=last_sum)



