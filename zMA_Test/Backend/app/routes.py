from zMA_Test.Backend.app import APP_MAIN
from flask import render_template, redirect,url_for,flash,send_file,request,json
from zMA_Test.Backend.practice.fetch_practice import fetch_easy_words


@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/practice')
def practice():
    status = {}
    words = fetch_easy_words()
    for word in words:
        status[word[0]] = "red"
        print("status ", word[0]);

    return render_template('practice.html', words=words, status=status)


@APP_MAIN.route('/test')
def test():
    return render_template('test.html')

@APP_MAIN.route('/clicked', methods=['POST'])
def translate():
    id= request.form['id']
    words = request.form['words'];
    wordID = request.form['wordid'];
    for word in words:
        print("word print in translate ", word[0][1])

    return json.dumps({'words': words})