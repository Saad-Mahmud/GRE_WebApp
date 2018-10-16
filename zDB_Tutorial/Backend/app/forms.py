from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from zDB_Tutorial.Backend.app.model import User
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.objects(username=username.data)
        if len(user):
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.objects(email=email.data)
        if len(user):
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=300)])
    submit = SubmitField('Submit')

class TestAjex(FlaskForm):
    about_me = TextAreaField('About me', validators=[Length(min=0, max=300)])
    about_me2 = TextAreaField('About me', validators=[Length(min=0, max=300)])