from zSaad_Test.Backend.app import APP_MAIN
from flask import render_template
from zSaad_Test.Backend.initDB.words import Words_Test



@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/dictionary')
def dictionary():
    wordlist=Words_Test.objects(wordID__startswith ='a_')
    print(wordlist[0].wordID)
    words = [
        {
            'word': w.word ,
            'TYPE': w.TYPE ,
            'meaning': w.meanings[0] ,
            'usages' : w.usages
        }
        for w in wordlist
    ]
    return render_template('dictionary.html', words=words)

