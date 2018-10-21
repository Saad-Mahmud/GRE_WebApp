from zMA_Test.Backend.app import APP_MAIN
from flask import render_template


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/practice')
def practice():
    return render_template('practice.html')


@APP_MAIN.route('/test')
def test():
    return render_template('test.html')