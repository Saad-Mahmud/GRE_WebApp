import json
import operator
import random
from datetime import datetime, timedelta
from random import randint

from flask import json, request, send_file
from flask import render_template, flash, redirect, url_for, abort, session, make_response
from flask_login import current_user, login_user, logout_user, login_required
from flask_oauth import OAuth
from flask_register import register_required
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

from zKM_Test.Backend.app import APP_MAIN, APPLOGIN, db, mail
from zKM_Test.Backend.app.forms import LoginForm, RegistrationForm, EditProfileForm, AdditionalForm, RequestResetForm, \
    ResetPasswordForm, LocalStatForm
from zKM_Test.Backend.app.model import User, Gre_data
from zMA_Test.Backend.app.model import session_test, session_practice, user_word_history
from zMA_Test.Backend.practice.fetch_practice import FetchWords, create_session_practice, create_user_word_history
from zMA_Test.Backend.practice.practice_util import showstat
from zMA_Test.Backend.test.adapter_pattern import Adapter
from zMA_Test.Backend.test.fetch_test import create_session_test, create_gre_test
from zMA_Test.Backend.test.test_util import show_test_stat
from zSaad_Test.Backend.words.words import Words

try:
    from urllib.request import Request,urlopen, URLError
except ImportError:
    from urllib2 import Request,urlopen,URLError
from os import urandom
from PIL import Image
from flask_mail import Message
next_gpage = ""
reg_bool = True
GOOGLE_CLIENT_ID = '375961356325-p3umdlkkjr6ak9kairqv8b3ttalio52a.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '8UggTqBUxM3M-9cd8KtLv8Tj'
REDIRECT_URI = '/oauth2callback'



oauth = OAuth()


google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)



@APP_MAIN.route('/gsign')
@APPLOGIN.header_loader
def gsign():
    global reg_bool
    reg_bool=False

    #access_token = session.get('access_token')
    if session.get('access_token') is None:
        print("access_token???")
        return redirect(url_for('login1'))
    access_token = session.get('access_token')[0]
    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    print(headers)
    print(req)

    try:
        res = urlopen(req)
        res = res.read().decode('utf-8')
        res = json.loads(res)
        uemail = res['email']

    except URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()
    user = User.objects(email=uemail)
    if len(user) == 0:
        print("painiiiii")
        session.pop('access_token',None)
        return redirect(url_for('login'))
    else:
        print("paiceeeeeeeeeeee")
        user = user[0]
        login_user(user)
        global next_gpage
        next_page = next_gpage
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)


@APP_MAIN.route('/login1')
def login1():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@APP_MAIN.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    print("ekhane ashco?")
    global reg_bool
    if reg_bool==False:
        return redirect(url_for('gsign'))
    else:
        return redirect(url_for('gregister'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


@APP_MAIN.route('/')
@APP_MAIN.route('/index')
def index():
    posts = [
        {
            'author': {'username':'Koushik Deb'},
            'body': 'Beautiful day in Malibagh'
        },
        {
            'author': {'username':'Sadeen Mahbub Mob'},
            'body': 'The Justice League movie was so khuul!'
        }
    ]
    return render_template('index.html', title = 'Home', posts=posts)


@APP_MAIN.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=generate_password_hash(form.password.data),reg_date=datetime.utcnow(), usertype='U', about_me=form.username.data+"\'s about")
        #reg_date = datetime.utcnow()-timedelta(days=15) will create reg date 15 days before now... so this will not come in admin page
        user.save()
        # gre_data = Gre_data(username=form.username.data)
        # gre_data.save()
        flash('Congratulation, you are now a member of GRE-Web App!!')
        session.pop('access_token', None)
        return redirect(url_for('additional',username=form.username.data))

    return render_template('register.html', title = 'Register', form=form)


@APP_MAIN.route('/gregister', methods=['POST','GET'])
def gregister():
    global reg_bool
    reg_bool = True
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login1'))
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
        res = res.read().decode('utf-8')
        res = json.loads(res)
        upic = res['picture']
        uemail = res['email']

    except URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('register'))
        return res.read()

    form = RegistrationForm()
    form.email.data=uemail
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=generate_password_hash(form.password.data),reg_date=datetime.utcnow(),upic=upic,usertype='U',about_me=form.username.data+"\'s about")
        user.save()
        gre_data = Gre_data(username=form.username.data)
        gre_data.save()
        flash('Congratulation, you are now a member of GRE-Web App!!')
        session.pop('access_token',None)
        return redirect(url_for('additional',username=form.username.data))

    return render_template('register.html', title = 'Register', form=form)


@APP_MAIN.route('/additional/<username>', methods=['POST','GET'])
@register_required
def additional(username):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AdditionalForm()

    collection = db['country']
    cursor = collection.find({})
    arr = []
    for i in cursor:
        arr.append(i['country_name'])
    if form.validate_on_submit():
        user = User.objects(username=username)
        #gre_data = Gre_data(username=username)
        name = username
        if len(user)==0:
            return render_template(url_for('login'))
        else:
            user = user[0]
        if user.check_password(form.confirm_password.data):
            user = user.update(age=form.age.data,
                               country=request.form.get('cnt_name'),
                               gender=form.gender.data)
            #gre_data = gre_data.update(country=request.form.get('cnt_name'),how_many_test=0,best_score=0,avg_score=0,rating=0)






            date = datetime.utcnow()
            create_gre_test(name, {}, date, 0, 0.0, 0.0, 0.0, request.form.get('cnt_name'), [], [], [])
            create_user_word_history(name)







            flash("Congrats!!you can now log in !!!")
            return redirect(url_for('login'))
        else:
            return redirect(url_for('index'))
    return render_template('additional.html',form=form , arr = arr)


@APP_MAIN.route('/login', methods=['POST','GET'])
def login():
    global next_gpage
    next_gpage = request.args.get('next')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data)
        if len(user)==0:
            return redirect(url_for('login'))
        else:
            user = user[0]
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title="Sign In", form=form)


@APP_MAIN.route('/about')
def about():
    return render_template('about.html', title = 'About')


@APP_MAIN.route('/logout')
def logout():
    resp = make_response(redirect(url_for('index')))
    if request.cookies.get('session'):
        resp.set_cookie('session', '', expires=0)
        session.pop('access_token',None)
    logout_user()
    return resp
    #return redirect(url_for('index'))


def rating(username):
    rate = Gre_data.objects(username=username)
    rate = rate[0]
    return rate


def ranking(ajax_var):
    col = db['gre_data']
    curser = col.find({})
    dict = {}
    dict1 = {}
    for i in curser:
        try:
            dict[i['_id']]= i['rating']
        except:
            dict[i['_id']]= 0
        user = User.objects(username=i['_id'])
        user = user[0]
        if ajax_var is None or ajax_var == 'select country' or ajax_var==current_user.country:
           if user.country == current_user.country:
               try:
                   dict1[i['_id']] = i['rating']
               except:
                   dict1[i['_id']] = 0
        else:
            if user.country == ajax_var:
                try:
                    dict1[i['_id']] = i['rating']
                except:
                    dict1[i['_id']] = 0
    sorted_global = sorted(dict.items(), key=operator.itemgetter(1),reverse=True)

    sorted_local = sorted(dict1.items(), key=operator.itemgetter(1),reverse=True)
    #print(sorted_global,sorted_local)
    return sorted_global,sorted_local
'''
@APP_MAIN.route('/statcountry',methods=['POST'])
@login_required
def statcountry():
    a = request.form['sc']
    print(a)
    col = db['gre_data']
    curser = col.find({})
    dict1 = {}
    for i in curser:
        user = User.objects(username=i['_id'])
        user = user[0]
        if user.country == a:
            dict1[i['_id']] = i['rating']
    sorted_local = sorted(dict1.items(), key=operator.itemgetter(1), reverse=True)


    return json.dumps({'status': sorted_local})
'''
@APP_MAIN.route('/user/<username>')
@login_required
def user(username):
    user = User.objects(username=username)
    if(len(user)==0):
        abort(404)
    else:
        user=user[0]
        if current_user.pic is not None:
            user.pic = url_for('static',filename='img/' + current_user.pic)
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    rate = rating(username)
    try:
        rank,local = ranking(current_user.country)
        for i in range(0,len(rank)):
            if rank[i][0]==current_user.username:
                rankindx = i + 1
                break
                print(rankindx)
        for i in range(0, len(local)):
            if local[i][0] == current_user.username:
                locindx = i+1
                break
                print(locindx)
    except:
        rankindx = None
        locindx = None

    return render_template('user.html', user=user, posts=posts, rate=rate, rankindx = rankindx, locindx=locindx)

def save_pic(form_picture):
    random_hex = urandom(8).hex()
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(APP_MAIN.static_folder, 'img', picture_fn)
    output_size=(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@APP_MAIN.route('/edit_profile',methods=['POST','GET'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_pic(form.pic.data)
            current_user.update(pic=picture_file)
        current_user.update(about_me=form.about_me.data)
        current_user.reload()
        flash("Your changes have been saved!")
        return redirect(url_for('user', username=current_user.username))
    elif request.method=='GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title="Edit Profile", form = form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
#     msg.body=f'''To reset your password visit following link:
# {url_for('reset_token', token=token, _external=True)}
# '''
    mail.send(msg)


@APP_MAIN.route('/reset_password',methods=['POST','GET'])
@login_required
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data)[0]
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@APP_MAIN.route('/reset_password/<token>',methods=['POST','GET'])
@login_required
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid token')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = user[0]
        password_hash=generate_password_hash(form.password.data)
        user = user.update(password_hash=password_hash)

        flash("Your password has been reset")
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Reset Password',form=form)


@APP_MAIN.route('/dictionary')
@login_required
def dictionary():
    pass


@login_required
@APP_MAIN.route('/testpage')
def test_page():
    return render_template("test_page.html")


@APP_MAIN.route('/test/<type>')
def test(type):
    dummy = FetchWords(current_user.username).practice_words(type,'test')
    listadapter = Adapter()
    test_words = listadapter.getList(dummy)
    status = {}
    ques_multi = []
    ques_blank = []
    sessionID = create_session_test(status, test_words, 0, ques_multi, ques_blank)
    pointer_f = session_test.objects(id=sessionID.id)[0]

    date = datetime.utcnow()
    pointer_f.words = test_words
    temp = Gre_data.objects(username=current_user.username)[0]

    print(test_words[0])
    random_idx = random.sample(range(1, 10), 3)
    option = []
    option_multiple_choice = []

    option.append(test_words[0][1])
    option_multiple_choice.append(test_words[0][2])
    print('amiiiiiiii', test_words[0][2])

    for i in range(3):
        option.append(test_words[random_idx[i]][1])
        option_multiple_choice.append(test_words[random_idx[i]][2])

    random_idx2 = random.sample(range(1, 5), 4)
    option_dict = {}
    option_multiple_choice_dict = {}

    for i in range(4):
        option_dict[option[i]] = random_idx2[i]
        option_multiple_choice_dict[option_multiple_choice[i]] = random_idx2[i]

    test_multi_choice_word = ''
    test_line = test_words[0][3]
    print(test_line)
    test_multi_choice_word += 'Meaning of '
    choice_word = test_words[0][1]
    choice_word = choice_word.upper()
    test_multi_choice_word += choice_word

    sorted_dict = sorted(option_dict.items(), key=operator.itemgetter(1))
    sorted_multi_choice_dict = sorted(option_multiple_choice_dict.items(), key=operator.itemgetter(1))

    test_line = test_line.replace(test_words[0][1], "___")
    ques_multi.append(test_multi_choice_word)
    ques_blank.append(test_line)

    pointer_f.ques_blank = ques_blank
    pointer_f.ques_multi = ques_multi

    pointer_f.save()

    return render_template('test_new.html', test_word=test_words[0], test_line=test_line,
                           multi_word=test_multi_choice_word, option_dict=sorted_dict,
                           multi_dict=sorted_multi_choice_dict, sessionID=sessionID.id)


@APP_MAIN.route('/nexttestword', methods=['POST'])
def nextTestWord():
    username = current_user.username
    answer = request.form['answer']
    sessionID = request.form['sessionID']
    isWhat = request.form['isWhat']

    pointer_f = session_test.objects(id=sessionID)[0]
    pointer = pointer_f.idx + 1
    test_words = pointer_f.words

    if isWhat == 'true':
        pointer_f.status[test_words[pointer_f.idx][1]] = answer
    else:
        test_words[pointer_f.idx][2] = test_words[pointer_f.idx][2].replace("."," ")
        test_words[pointer_f.idx][2] = test_words[pointer_f.idx][2].replace("$", " ")
        pointer_f.status[test_words[pointer_f.idx][2]] = answer

    pointer_f.idx = pointer
    pointer_f.save()

    if pointer < len(test_words):
        test_word = test_words[pointer]
        option = []

        if isWhat == 'true':
            option.append(test_word[1])
        else:
            option.append(test_word[2])

        if pointer <= 3:
            random_idx1 = random.sample(range(0, pointer), 1)
            random_idx2 = random.sample(range(pointer + 1, 10), 2)
            random_idx = random_idx1 + random_idx2
        elif pointer <= 7:
            random_idx1 = random.sample(range(0, pointer), 2)
            random_idx2 = random.sample(range(pointer + 1, 10), 1)
            random_idx = random_idx1 + random_idx2
        else:
            random_idx = random.sample(range(0, pointer), 3)

        for i in range(3):
            if isWhat == 'true':
                option.append(test_words[random_idx[i]][1])
            else:
                option.append(test_words[random_idx[i]][2])

        random_idx_option = random.sample(range(1, 5), 4)
        option_dict = {}

        for i in range(4):
            option_dict[option[i]] = random_idx_option[i]

        sorted_dict = sorted(option_dict.items(), key=operator.itemgetter(1))
        correct, wrong = show_test_stat(pointer_f.status)
        if isWhat == 'true':
            test_line = test_word[3]
            test_line = test_line.replace(test_word[1], "___")
            pointer_f.ques_blank.append(test_line)

            pointer_f.save()
            return json.dumps({'test_word': test_word, 'test_line': test_line, 'option_dict': sorted_dict, 'correct': correct, 'wrong': wrong})
        else:
            test_multi_choice_word = ''
            test_multi_choice_word += 'Meaning of '
            choice_word = test_word[1]
            choice_word = choice_word.upper()
            test_multi_choice_word += choice_word
            pointer_f.ques_multi.append(test_multi_choice_word)
            pointer_f.save()
            return json.dumps({'test_word': test_word, 'test_line': test_multi_choice_word, 'option_dict': sorted_dict, 'correct': correct, 'wrong': wrong})

    else:
        test_word = ['$null$']
        session_data = session_test.objects(id=sessionID)[0]
        print("abcdefgh", session_data.status)
        test_key = 'test' + sessionID
        gre_test_words = {
            test_key: session_data.status
        }

        correct, wrong = show_test_stat(pointer_f.status)
        print(correct, wrong)

        gre_data = Gre_data.objects(username=username)[0]
        print(gre_data.username)
        gre_data.history[test_key] = session_data.status
        gre_data.test_date = datetime.utcnow()
        gre_data.how_many_test = gre_data.how_many_test + 1

        current_score = correct * 10

        if gre_data.best_score < current_score:
            gre_data.best_score = current_score

        gre_data.rating = gre_data.rating + current_score
        gre_data.avg_score = gre_data.rating / gre_data.how_many_test

        gre_data.rating_chart.append(gre_data.rating)
        gre_data.rate_date.append(gre_data.test_date)
        gre_data.all_scores.append(current_score)

        gre_data.save()
        pointer_f.save()

        return json.dumps({'test_word': test_word, 'correct': correct, 'wrong': wrong})


@APP_MAIN.route('/thisans', methods=['POST'])
def nextAns():
    sessionID = request.form['sessionID']
    isWhat = request.form['isWhat']

    pointer_f = session_test.objects(id=sessionID)[0]
    test_words = pointer_f.words


    if isWhat == 'true':
        answer = test_words[pointer_f.idx][1]
    else:
        answer = test_words[pointer_f.idx][2]

    return json.dumps({'ans': answer})


@APP_MAIN.route('/testsummary', methods=['POST'])
def summary():
    sessionID = request.form['sessionID']
    print(sessionID)
    isWhat = request.form['isWhat']
    print(isWhat)
    correct = request.form['correct']
    print(correct)
    wrong = request.form['wrong']
    print(wrong)

    pointer_f = session_test.objects(id=sessionID)[0]
    test_words = pointer_f.words

    if isWhat=='true':
        ques = pointer_f.ques_blank
    else:
        ques = pointer_f.ques_multi

    status = pointer_f.status
    correct_ans=[]
    your_ans=[]

#if it does not work,, change status.iteritems() to status.items() or vice versa
    for the_key, the_value in status.items():
        correct_ans.append(the_key)
        your_ans.append(the_value)

    return render_template("test_summary.html", correct=correct, wrong=wrong, isWhat=isWhat,
                           test_words=test_words, ques=ques, correct_ans=correct_ans, your_ans=your_ans)


@login_required
@APP_MAIN.route('/practice')
def practice_intro():
    return render_template("practice.html")


@APP_MAIN.route('/practice/<type>')
def practice(type):
    print("type ", type)
    fetchwords = FetchWords(current_user.username)
    words = fetchwords.practice_words(type,"practice")
    status = {word['wordID']:'firstseen' for word in words}
    sessionID = create_session_practice(status, words, 0)
    #userWordHistory = create_user_word_history()

    return render_template('tryit.html', word=words[0], sessionID=sessionID.id)


@APP_MAIN.route('/fliped', methods=['POST'])
def translate():
    sessionID = request.form['sessionID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    pointer = pointer_f.idx # fetched pointer
    words = pointer_f.words # fetched word list

    if len(words)!=0:
        word = words[pointer]
    else:
        word = {'wordID':"$null$"}

    return json.dumps({'word': word})





@APP_MAIN.route('/nextword', methods=['POST'])
def nextWord():

    #user_history = user_word_history.objects(username="moumita")[0]
    user_history = user_word_history.objects(username=current_user.username)[0]
    sessionID = request.form['sessionID']
    buttonID = request.form['buttonID']
    pointer_f = session_practice.objects(id=sessionID)[0]

    pointer = pointer_f.idx # fetched, incremented pointer, saved the incremented pointer
    words = pointer_f.words
    oldStatus = pointer_f.status
    newStatus = oldStatus
    currentWord = words[pointer]
    currentWordID = currentWord['wordID']

    if buttonID=='ik':
        if newStatus[currentWordID]=='firstseen':
            newStatus[currentWordID] = 'yellow'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand, currentWord)

        elif newStatus[currentWordID]=='red':
            newStatus[currentWordID] = 'yellow'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand,currentWord)

        elif newStatus[currentWordID]=='yellow':
            newStatus[currentWordID] = 'green'
            words.remove(currentWord)

    elif buttonID=='idk':
        if newStatus[currentWordID]=='firstseen':
            newStatus[currentWordID] = 'red'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand, currentWord)

        elif newStatus[currentWordID]=='yellow':
            newStatus[currentWordID]='yellow'
            words.remove(currentWord)
            rand = randint(0, len(words))
            words.insert(rand, currentWord)

    if len(words) != 0:
        pointer = (pointer + 1) % len(words)
        newWord = words[pointer]
        pointer_f.words = words
        pointer_f.status = newStatus
        pointer_f.idx = pointer
        pointer_f.save()
    else:
        pointer = -1
        newWord = {'wordID': '$null$'}


    print("word status ",  newStatus[currentWordID])
    user_history.status[currentWordID] = newStatus[currentWordID]
    user_history.save()
    mastered, reviewing, learning = showstat(newStatus)

    return json.dumps({'word': newWord, 'learning': learning, 'reviewing':reviewing, 'mastered':mastered})


@APP_MAIN.route('/tryit')
def tryit():
    return render_template('flashcard.html')

import os
static_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
static_dir = os.path.join(static_dir, 'Frontend')
static_dir = os.path.join(static_dir, 'static')
static_dir = os.path.join(static_dir, 'audio')

@APP_MAIN.route('/words/audio/',defaults={'filename': ''})
@APP_MAIN.route('/words/audio/<path:filename>')
def download_file(filename):
    file = ''
    for i in range(len(filename)-4):
        file =file+filename[i]
    print(file)
    filename = os.path.join(static_dir, filename)
    if(Words.objects(word=file)==[]):
        return
    return send_file(filename)



















@APP_MAIN.route('/stat',methods=['POST','GET'])
@login_required
def stat():
    collection = db['country']
    cursor = collection.find({})
    arr = []
    for i in cursor:
        arr.append(i['country_name'])


    cursor1 = db['user'].find({})
    ajax_var = request.form.get('cnt_name1')
    print(ajax_var)
    rank, local = ranking(ajax_var)
    form = LocalStatForm()
    stat_data = Gre_data.objects(username=current_user.username)
    stat_data = stat_data[0]
    user = User

    #print(cursor1[10]['_id']==stat_data.id)
    return render_template('stat.html', stat_data=stat_data,
                           user=user,rank = rank,ajax_var=ajax_var,
                           local=local,length=len(rank),length1=len(local), arr=arr, form = form)


@APP_MAIN.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated:
        if current_user.usertype=='A':
            current_time1 = datetime.now()
            lastweek = datetime.now() - timedelta(days=7)
            print(lastweek)
            cursor = db['user'].find({})
            dict = {}
            for i in cursor:
                if i['reg_date']>lastweek:
                    dict[i['_id']] = i['reg_date']

            print(type(dict))
            return render_template('history.html', dict = dict)
    return redirect(url_for('index'))



@APP_MAIN.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update(last_seen=datetime.utcnow())
        current_user.reload()