import json
from datetime import datetime, timedelta

from flask import json, request
from flask import render_template, flash, redirect, url_for, abort, session, make_response
from flask_login import current_user, login_user, logout_user, login_required
from flask_oauth import OAuth
from flask_register import register_required
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse

from App_Main.Backend.App import APP_MAIN, APPLOGIN, db, mail
from zKM_Test.Backend.app.forms import LoginForm, RegistrationForm, EditProfileForm, RequestResetForm,  ResetPasswordForm, LocalStatForm
from zKM_Test.Backend.builder import RegBuilder, AdapterPattern, ProfileAdapter, EditProfileBuilder
from zKM_Test.Backend.factory.LoginFactory import LoginFactory
from zKM_Test.Backend.factory.RateRank import RateRank as RK
from zKM_Test.Backend.facade.facadeForm import AdditionalForm
from zKM_Test.Backend.app.model import User, Gre_data, Country
from zKM_Test.Backend.facade import FacadeAdditional
from zKM_Test.Backend.iterator.StatIterator import Iteration

try:
    from urllib.request import Request,urlopen, URLError
except ImportError:
    from urllib2 import Request,urlopen,URLError

from flask_mail import Message

next_gpage = ""
reg_bool = True
GOOGLE_CLIENT_ID = '375961356325-p3umdlkkjr6ak9kairqv8b3ttalio52a.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '8UggTqBUxM3M-9cd8KtLv8Tj'
REDIRECT_URI = '/oauth2callback'



oauth = OAuth()
RateRank = RK()

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


@APP_MAIN.route('/index')
@login_required
def index():
    posts = []
    return render_template('index.html', title = 'Home', posts=posts)


@APP_MAIN.route('/register', methods=['POST','GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        Concrete_Builder = RegBuilder.ConcreteBuilder()
        director = RegBuilder.Director(form = form)
        director.construct(Concrete_Builder)
        user1 = Concrete_Builder.product
        # user = User(username=form.username.data,
        #             email=form.email.data,
        #             password_hash=generate_password_hash(form.password.data),reg_date=datetime.utcnow(), usertype='U', about_me=form.username.data+"\'s about")
        # user.save()
        user = AdapterPattern.Adapter()
        user = user.request(user1)
        user.save()

        # reg_date = datetime.utcnow()-timedelta(days=15) will create reg date 15 days before now... so this will not come in admin page
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

    cntttt = ["America", "Argentina", "Australia", "Bangladesh", "Brazil", "China", "England",
              "Honululu", "India", "Japan", "Nepal", "Pakistan",
              "Russia", "Sri Lanka", "Syria", "Uganda"
              ]

    for i in range(1, 17, 1):
        cnt = Country(country_id=i,
                      country_name=cntttt[i - 1])
        cnt.save()

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = AdditionalForm()

#    ///////////////////////Iterator pattern///////////////////////////////
    arr = Iteration()
    arr = arr.IteratingCountry()
    if form.validate_on_submit():
        # /////////////////////////facade pattern //////////////////////////////
        facade = FacadeAdditional.Addition(username=username,form=form)
        facade = facade.additionalInfo()
        if facade==True:
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
        # user = User.objects(username=form.username.data)
        # if len(user)==0:
        #     return redirect(url_for('login'))
        # else:
        #     user = user[0]
        # if user is None or not user.check_password(form.password.data):
        #     return redirect(url_for('login'))
        # login_user(user,remember=form.remember_me.data)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)
        log = LoginFactory()
        red = log.CheckValid(form)
        return redirect(red)
    return render_template('login.html',title="Sign In", form=form)




@APP_MAIN.route('/logout')
@login_required
def logout():
    resp = make_response(redirect(url_for('hello_world')))
    if request.cookies.get('session'):
        resp.set_cookie('session', '', expires=0)
        session.pop('access_token',None)
    logout_user()
    return resp
    #return redirect(url_for('index'))





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

    rate = RateRank.rating(username)

    try:
        rank,local = RateRank.ranking(current_user.country)
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
    stat_data = Gre_data.objects(username=current_user.username)
    stat_data = stat_data[0]

    return render_template('user.html', user=user, posts=posts, rate=rate, rankindx = rankindx, locindx=locindx,stat_data=stat_data, title='Profile')

# def save_pic(form_picture):
#     random_hex = os.urandom(8).hex()
#     _,f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(APP_MAIN.static_folder, 'img', picture_fn)
#     output_size=(125,125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn

@APP_MAIN.route('/edit_profile',methods=['POST','GET'])

@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        # if form.pic.data:
        #     picture_file = save_pic(form.pic.data)
        #     current_user.update(pic=picture_file)
        # current_user.update(about_me=form.about_me.data)
        Concrete_Builder = EditProfileBuilder.ConcreteBuilder()
        director = EditProfileBuilder.Director(form=form)
        director.construct(Concrete_Builder)
        user1 = Concrete_Builder.product
        user = ProfileAdapter.Adapter()
        user.request(user1)
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



#.............................. Amit Routes starts-------------------------------------


#.............................. Amit Routes ends-------------------------------------


#.............................. Moumita Routes starts-------------------------------------


#.............................. Moumita Routes ends-------------------------------------

@APP_MAIN.route('/stat',methods=['POST','GET'])
@login_required
def stat():

#    ///////////////////////Iterator pattern///////////////////////////////
    arr = Iteration()
    arr = arr.IteratingCountry()

    cursor1 = db['user'].find({})
    ajax_var = request.form.get('cnt_name1')
    print(ajax_var)
    rank, local = RateRank.ranking(ajax_var)
    form = LocalStatForm()
    stat_data = Gre_data.objects(username=current_user.username)
    stat_data = stat_data[0]
    user = User

    #print(cursor1[10]['_id']==stat_data.id)
    return render_template('stat.html', stat_data=stat_data,
                           user=user,rank = rank,ajax_var=ajax_var,
                           local=local,length=len(rank),length1=len(local), arr=arr, form = form, title='Statistics')


@APP_MAIN.route('/admin_stat')
@login_required
def admin():
    if current_user.is_authenticated and current_user.usertype=='A':
            current_time1 = datetime.now()
            lastweek = datetime.now() - timedelta(days=7)
            print(lastweek)
            cursor = db['user'].find({})
            dict = {}
            for i in cursor:
                if i['reg_date']>lastweek:
                    dict[i['_id']] = i['reg_date']

            return render_template('history.html', dict = dict)
    return redirect(url_for('index'))



@APP_MAIN.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update(last_seen=datetime.utcnow())
        current_user.reload()