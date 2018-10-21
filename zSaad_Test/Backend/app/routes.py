from zSaad_Test.Backend.app import APP_MAIN
from flask import render_template
from zSaad_Test.Backend.initDB.words import Words_Test



@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")


@APP_MAIN.route('/dictionary/',defaults={'page': 'ALL'})
@APP_MAIN.route('/dictionary/<string:page>')
def dictionary(page):
    page = page.lower()
    title = page.capitalize()
    links = ['All','A','B','C','D','E','F','G'
        ,'H','I','J','K','L','M','N','O','P',
             'Q','R','S','T','U','V','W','X','Y','Z']
    print(title)
    if(page=='all'):
        wordlist=Words_Test.objects
    elif(page[0]>='a' and page[0]<='z' and len(page)==1):
        wordlist = Words_Test.objects(wordID__startswith=page[0])
    else:
        return render_template('404.html')
    words = [
        {
            'word': w.word ,
            'TYPE': w.TYPE ,
            'meaning': w.meanings[0] ,
            'usages' : w.usages
        }
        for w in wordlist
    ]
    return render_template('dictionary.html',links=links, title=title, words=words)

