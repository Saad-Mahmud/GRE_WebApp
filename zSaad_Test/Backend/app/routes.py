from zSaad_Test.Backend.app import APP_MAIN
from flask import render_template,redirect,url_for,flash,send_file,request,json
from zSaad_Test.Backend.initDB.words import Words_Test
from zSaad_Test.Backend.app.forms import WordSuggestionForm
import os

static_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
static_dir = os.path.join(static_dir, 'Frontend')
static_dir = os.path.join(static_dir, 'static')
static_dir = os.path.join(static_dir, 'audio')

@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")

@APP_MAIN.route('/words/audio/',defaults={'filename': ''})
@APP_MAIN.route('/words/audio/<path:filename>')
def download_file(filename):
    file = ''
    for i in range(len(filename)-4):
        file =file+filename[i]
    print(file)
    filename = os.path.join(static_dir, filename)
    if(Words_Test.objects(word=file)==[]):
        return
    return send_file(filename)

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
    print(wordlist)

    words = [
        {
            'wordID': w.wordID,
            'word': w.word ,
            'TYPE': w.TYPE ,
            'meaning': w.meanings[0] ,
            'usages' : w.usages
        }
        for w in wordlist
    ]
    return render_template('dictionary.html',links=links, title=title, words=words)

@APP_MAIN.route('/suggestions/words/',defaults={'wordID': ''},methods=['GET', 'POST'])
@APP_MAIN.route('/suggestions/words/<string:wordID>',methods=['GET', 'POST'])
def suggestion(wordID):
    if(wordID==''):
        return render_template('404.html')
    elif(Words_Test.objects(wordID=wordID)==[]):
        return render_template('404.html')

    form = WordSuggestionForm()
    if form.validate_on_submit():
        print (form.TYPE.data)
        print (form.report.data)
        flash('Report Submitted!')
        return redirect(url_for('dictionary')+wordID[0])
    return render_template('suggestions_word.html', form=form)


@APP_MAIN.route('/translate', methods=['POST'])
def translate():
    s1= request.form['data']
    print("s1: "+s1)
    return json.dumps({'status': s1})


@APP_MAIN.route('/adminwords/',defaults={'page': 'ALL'})
@APP_MAIN.route('/adminwords/<string:page>')
def admin_words(page):
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
            'wordID': w.wordID,
            'word': w.word ,
            'TYPE': w.TYPE ,
            'meaning': w.meanings[0] ,
            'usages' : w.usages
        }
        for w in wordlist
    ]
    return render_template('admin_words.html',links=links, title=title, words=words)
