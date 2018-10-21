from zDB_Tutorial.Backend.app import APP_MAIN, APPLOGIN
from flask import render_template, flash,redirect,url_for,abort
from zDB_Tutorial.Backend.app.forms import LoginForm , RegistrationForm , EditProfileForm, TestAjex
from flask_login import current_user, login_user, logout_user , login_required
from zDB_Tutorial.Backend.app.model import User
from flask import request
from werkzeug.urls import url_parse
from werkzeug.security import generate_password_hash
from datetime import datetime
import json


@APP_MAIN.route('/')
@APP_MAIN.route('/index')
@login_required
def index():
    user = {'username': 'Saad'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)



@APP_MAIN.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data)
        if(len(user)==0):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            user = user[0]
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@APP_MAIN.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@APP_MAIN.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=generate_password_hash(form.password.data))
        user.save()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@APP_MAIN.route('/user/<username>')
@login_required
def user(username):
    user = User.objects(username=username)
    if(len(user)==0):
        abort(404)
    else:
        user=user[0]
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@APP_MAIN.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.update(last_seen = datetime.utcnow())
        current_user.reload()


@APP_MAIN.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.update(about_me = form.about_me.data)
        current_user.reload()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@APP_MAIN.route('/testajax', methods=['GET', 'POST'])
@login_required
def test_ajax():
    form = TestAjex()
    if form.validate_on_submit():
        print(form.about_me.data)
        print(form.about_me2.data)
    return render_template('ajaxtest.html', title='Test Ajax',
                           form=form)


@APP_MAIN.route('/here', methods=['POST'])
def kaka():
    s1=  request.form['about_me']
    s2 = request.form['about_me2']
    print("s1: "+s1+s2)
    return json.dumps({'status': s1+s2})