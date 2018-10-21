from zMA_Test.Backend.app import APP_MAIN
from flask import render_template
from zMA_Test.Backend.practice.fetch_practice import fetch_easy


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/practice')
def practice():
    fetch_easy()
    return render_template('practice.html')


@APP_MAIN.route('/test')
def test():
    return render_template('test.html')