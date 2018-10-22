from zMA_Test.Backend.app import APP_MAIN
from flask import render_template
from zMA_Test.Backend.practice.fetch_practice import fetch_easy_words


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/practice')
def practice():
    words = fetch_easy_words()
    counter = []
    for idx in range(0, len(words)):
        counter.append(idx)

    return render_template('practice.html', words=words, counter=counter)


@APP_MAIN.route('/test')
def test():
    return render_template('test.html')