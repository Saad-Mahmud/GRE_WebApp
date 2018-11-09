import json

from flask import render_template, request
from flask_login import login_required, current_user

from App_Main.Backend.App import APP_MAIN
from zKM_Test.Backend.observer.Observer1 import Notification
from zMA_Test.Backend.practice.fetch_practice import FetchWords
from zMA_Test.Backend.test.adapter_pattern import Adapter
from zMA_Test.Backend.test.builder_pattern import ConcreteBuilder, Director
from zMA_Test.Backend.test.builder_pattern_summary import ConcreteBuilderSummary, DirectorSummary
from zMA_Test.Backend.test.fetch_test import create_session_test, update_initial_session_test, update_next_session_test, \
    update_gre_data, update_test_summary
from zMA_Test.Backend.test.memento_pattern import Caretaker, Originator
from zMA_Test.Backend.test.test_util import show_test_stat, rating_change


@APP_MAIN.route('/testpage')
@login_required
def test_page():
    return render_template("test_page.html")


@APP_MAIN.route('/test/<type>')
@login_required
def test(type):
#...................................................Factory Pattern is used...............................................
    dummy = FetchWords(current_user.username).practice_words(type, 'test')

#...................................Adapter Pattern is used to convert dictionary to a list...............................
    listadapter = Adapter()
    test_words = listadapter.request(dummy)

    status = {}
    ques_multi = []
    ques_blank = []
    sessionID = create_session_test(status, test_words, 0, ques_multi, ques_blank)
    test_word = test_words[0]
    temp_test_words1 = []
    temp_test_words2 = []

    for i in range(10):
        temp_test_words1.append(test_words[i][1])
        temp_test_words2.append(test_words[i][2])

#..................................................Builder pattern is used..............................................
    concrete_builder = ConcreteBuilder()
    director = Director(test_word[1], 0, temp_test_words1, test_word[3], test_word[1], test_word[1])
    director.construct(concrete_builder, 1)
    check1 = concrete_builder.option_object

    concrete_builder = ConcreteBuilder()
    director = Director(test_word[2], 0, temp_test_words2, test_word[3], test_word[1], test_word[1])
    director.construct(concrete_builder, 1)
    check2 = concrete_builder.option_object
    update_initial_session_test(sessionID, test_words, check1.test_line, check2.test_multi_choice_word)

    return render_template('test_new.html', test_word=test_words[0], test_line=check1.test_line,
                           multi_word=check2.test_multi_choice_word, option_dict=check1.sorted_dict,
                           multi_dict=check2.sorted_dict, sessionID=sessionID.id)


@APP_MAIN.route('/nexttestword', methods=['POST'])
@login_required
def nextTestWord():
    username = current_user.username
    answer = request.form['answer']
    sessionID = request.form['sessionID']
    isWhat = request.form['isWhat']

    test_words, pointer = update_next_session_test(sessionID, isWhat, answer, 1, ' ')
    if pointer < len(test_words):
        test_word = test_words[pointer]
        temp_test_words1 = []
        temp_test_words2 = []

        for i in range(10):
            temp_test_words1.append(test_words[i][1])
            temp_test_words2.append(test_words[i][2])

#.................................................Builder Pattern is used.................................................
        if isWhat == 'true':
            concrete_builder = ConcreteBuilder()
            director = Director(test_word[1], pointer, temp_test_words1, test_word[3], test_word[1], test_word[1])
            director.construct(concrete_builder, 2)
            check = concrete_builder.option_object

            status = update_next_session_test(sessionID, isWhat, answer, 2, check.test_line)
            correct, wrong = show_test_stat(status)
            return json.dumps({'test_word': test_word, 'test_line': check.test_line, 'option_dict': check.sorted_dict, 'correct': correct, 'wrong': wrong})

        else:
            concrete_builder = ConcreteBuilder()
            director = Director(test_word[2], pointer, temp_test_words2, test_word[3], test_word[1], test_word[1])
            director.construct(concrete_builder, 2)
            check = concrete_builder.option_object

            status = update_next_session_test(sessionID, isWhat, answer, 3, check.test_multi_choice_word)
            correct, wrong = show_test_stat(status)

            return json.dumps({'test_word': test_word, 'test_line': check.test_multi_choice_word, 'option_dict': check.sorted_dict, 'correct': correct, 'wrong': wrong})

    else:
        test_word = ['$null$']
        session_data = update_next_session_test(sessionID, isWhat, answer, 6, ' ')
        test_key = 'test' + sessionID
        status = update_next_session_test(sessionID, isWhat, answer, 4, ' ')
        correct, wrong = show_test_stat(status)
        update_gre_data(username, test_key, session_data, correct)
        observeKM = Notification()
        observeKM.Ovserved()
        rating_change(status, test_words)

        return json.dumps({'test_word': test_word, 'correct': correct, 'wrong': wrong})


@APP_MAIN.route('/thisans', methods=['POST'])
@login_required
def nextAns():
    sessionID = request.form['sessionID']
    isWhat = request.form['isWhat']
    answer = update_next_session_test(sessionID, isWhat, ' ', 5, ' ')

    return json.dumps({'ans': answer})


@APP_MAIN.route('/testsummary', methods=['POST'])
@login_required
def summary():
    sessionID = request.form['sessionID']
    isWhat = request.form['isWhat']
    correct = request.form['correct']
    wrong = request.form['wrong']
    pointer_f = update_next_session_test(sessionID, isWhat, ' ', 6, ' ')

#......................................Builder pattern is used to build the summary..........................................
    concrete_builder = ConcreteBuilderSummary()
    director = DirectorSummary(pointer_f, isWhat)
    director.constructSummary(concrete_builder)
    check = concrete_builder.summary_object

# .....................................Memento pattern is used to save the summary...........................................
    prev_sum = update_test_summary(current_user.username, check.ques, check.your_ans, check.correct_ans)
    caretaker = Caretaker()
    originator = Originator()
    originator.setState(prev_sum)
    caretaker.addMemento(originator.save())

    return render_template("test_summary.html", correct=correct, wrong=wrong, isWhat=isWhat,
                           test_words=check.test_words, ques=check.ques, correct_ans=check.correct_ans, your_ans=check.your_ans)


@APP_MAIN.route('/previoussummary')
@login_required
def previoussummary():
#.......................................Memento Pattern is used to restore the summary......................................
    caretaker = Caretaker()
    originator = Originator()
    if caretaker.mementos.__len__() > 0:
        last_sum = originator.restore(caretaker.getMemento(caretaker.mementos.__len__() - 1))
        return render_template("test_prev_summary.html", last_sum=last_sum, memento_len=caretaker.mementos.__len__())
    else:
        return render_template("test_no_summary.html")


@APP_MAIN.route('/definedprevsum', methods=['POST'])
@login_required
def definedprevsum():
    sumpath = request.form['summarypath']
#............................................Memento is used to restore a defined summary....................................
    caretaker = Caretaker()
    originator = Originator()
    if int(sumpath) < 0:
        return render_template("test_no_summary.html")
    if int(sumpath) > caretaker.mementos.__len__():
        return render_template("test_no_summary.html")
    else:
        last_sum = originator.restore(caretaker.getMemento(int(sumpath)-1))
        return render_template("test_prev_summary.html", last_sum=last_sum)