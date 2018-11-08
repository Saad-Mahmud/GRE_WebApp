from zSaad_Test.Backend.app import APP_MAIN
from flask import render_template,redirect,url_for,flash,send_from_directory,request,json
from zSaad_Test.Backend.Words.Words import Words
from werkzeug.utils import secure_filename
from zSaad_Test.Backend.app.model import Suggestions
import datetime

import os
try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve



@APP_MAIN.route('/')
def hello_world():
    return render_template("dummy.html")

@APP_MAIN.route('/Words/audio/',defaults={'filename': ''})
@APP_MAIN.route('/Words/audio/<path:filename>')
def download_file(filename):
    file = ''
    for i in range(len(filename)-4):
        file =file+filename[i]
    print(file)
    if(Words.objects(word=file)==[]):
        return
    return send_from_directory(APP_MAIN.config['AUDIO_FOLDER'],
                               filename)

@APP_MAIN.route('/dictionary/',defaults={'page': 'ALL'})
@APP_MAIN.route('/dictionary/<string:page>')
def dictionary(page):
    page = page.lower()
    title = page.capitalize()
    links = ['All','A','B','C','D','E','F','G'
        ,'H','I','J','K','L','M','N','O','P',
             'Q','R','S','T','U','V','W','X','Y','Z']

    if(page=='all'):
        wordlist=Words.objects
    elif(page[0]>='a' and page[0]<='z' and len(page)==1):
        wordlist = Words.objects(wordID__startswith=page[0])
    else:
        return render_template('404.html')


    words = [
        {
            'wordID': w.wordID,
            'word': w.word ,
            'TYPE': w.TYPE ,
            'meaning': w.meanings[0] ,
            'usages' : w.usages ,
            'translations' : w.translations
        }
        for w in wordlist
    ]
    return render_template('dictionary.html',links=links, title=title, words=words,length=len(words))

@APP_MAIN.route('/suggestions/Words/',defaults={'wordID': ''})
@APP_MAIN.route('/suggestions/Words/<string:wordID>')
def suggestion(wordID):
    if(wordID==''):
        return render_template('404.html')
    elif(len(Words.objects(wordID=wordID))==0):
        return render_template('404.html')

    return render_template('suggestions_word.html', form=['Translation','Meaning','Usage','Error'])

@APP_MAIN.route('/suggestions/general/',defaults={'x': ''})
@APP_MAIN.route('/suggestions/general/<string:x>')
def suggestion2(x):
    if(x!=""):
        return render_template("404.html")
    return render_template('suggestions_word.html', form=['New Word','Bug'])

@APP_MAIN.route('/processsuggestion', methods=['POST'])
def processsuggestion():
    tp = request.form['type']
    report = request.form['report']
    date = str(datetime.datetime.now())
    status = 'US'
    Suggestions(TYPE=tp,report=report,date=date,status=status).save()
    return json.dumps({'status': 'success'})

@APP_MAIN.route('/translate', methods=['POST'])
def translate():
    s1= request.form['data']
    print("s1: "+s1)
    return json.dumps({'status': s1})

@APP_MAIN.route('/admindelete/',defaults={'delid':''})
@APP_MAIN.route('/admindelete/<string:delid>')
def admindelete(delid):
    if (len(Words.objects(wordID=delid)) == 0):
        return render_template('404.html')
    return render_template('deleteword.html', word = Words.objects(wordID=delid)[0])


@APP_MAIN.route('/admintranslate/',defaults={'trnsid':''})
@APP_MAIN.route('/admintranslate/<string:trnsid>')
def admintranslate(trnsid):
    if (len(Words.objects(wordID=trnsid)) == 0):
        return render_template('404.html')
    return render_template('admintranslate.html', word = Words.objects(wordID=trnsid)[0])



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
        wordlist=Words.objects
    elif(page[0]>='a' and page[0]<='z' and len(page)==1):
        wordlist = Words.objects(wordID__startswith=page[0])
    else:
        return render_template('404.html')
    words = [
        {
            'wordID': w.wordID,
            'word': w.word ,
            'TYPE': w.TYPE ,
            'meaning': w.meanings[0] ,
            'usages' : w.usages ,
            'translations': w.translations
        }
        for w in wordlist
    ]
    return render_template('admin_words.html',links=links, title=title, words=words,length=len(words))

@APP_MAIN.route('/admindeleteword', methods=['POST'])
def admindeleteword():
    s1= request.form['wordID']
    if(len(Words.objects(wordID=s1)) == 0):
        return json.dumps({'status': 'success'})
    else:
        print("here")
        Words.objects(wordID=s1)[0].delete()
        return json.dumps({'status': 'success'})

@APP_MAIN.route('/adminaddtrans', methods=['POST'])
def adminaddtrans():
    lang= request.form['Lang']
    trans = request.form['Trans']
    wordID = request.form['id']

    if(len(Words.objects(wordID=wordID)) == 0):
        return json.dumps({'status': 'success'})
    else:
        print("here")
        a = Words.objects(wordID=wordID)[0]
        print(a.word)
        a.translations[lang] = trans
        
        a.save()
        return json.dumps({'status': 'success'})


@APP_MAIN.route('/admineditword/',defaults={'wordID':''})
@APP_MAIN.route('/admineditword/<string:wordID>')
def admineditword(wordID):
    return render_template('editwordpage.html')

@APP_MAIN.route('/adminnewword/')
def adminnewword():
    return render_template('addnewword.html')


@APP_MAIN.route('/adminaudio/',defaults={'wordID':''},methods=['POST','GET'])
@APP_MAIN.route('/adminaudio/<string:wordID>',methods=['POST','GET'])
def adminaudio(wordID):

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename_ = secure_filename(file.filename)
            if(filename_!=file.filename):
                return redirect(request.url)
            file.save(os.path.join(APP_MAIN.config['AUDIO_FOLDER'], filename_))
            return redirect(url_for('admin_words'))
    else:
        if (len(Words.objects(wordID=wordID)) == 0):
            return render_template('404.html')
        return render_template('adminaudio.html', word = Words.objects(wordID=wordID)[0])

ALLOWED_EXTENSIONS = ['mp3', 'mpeg']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@APP_MAIN.route('/adminsuggestions/',defaults={'x':''})
@APP_MAIN.route('/adminsuggestions/<string:x>')
def adminsuggestions(x):
    if(x!=''):
        return render_template('404.html')
    a = Suggestions.objects(status='US')
    return render_template('adminsuggestions.html',suggestions=a,length=len(a))

@APP_MAIN.route('/admintodo/',defaults={'x':''})
@APP_MAIN.route('/admintodo/<string:x>')
def admintodo(x):
    if(x!=''):
        return render_template('404.html')
    a = Suggestions.objects(status='TD')
    return render_template('admintodo.html',suggestions=Suggestions.objects(status='TD'),length=len(a))

@APP_MAIN.route('/editsuggestion', methods=['POST'])
def editsuggestion():
    if(request.form['type']=='todo'):
        a = Suggestions.objects(id=request.form['id'])

        if(len(a)):
            k = a[0]
            k.status = 'TD'
            k.save()
    elif(request.form['type']=='del'):
        a = Suggestions.objects(id=request.form['id'])
        if (len(a)):
            a = a[0]
            a.delete()
    return json.dumps({'status': 'success'})
