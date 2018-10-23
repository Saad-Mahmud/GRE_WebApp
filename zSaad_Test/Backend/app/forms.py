from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, TextAreaField, SubmitField,RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
try:
    from appdirs import unicode
except ImportError:
    print (ImportError)

class WordSuggestionForm(FlaskForm):
    report = TextAreaField('Report', validators=[DataRequired(),Length(min=20, max=300)])

    TYPE = RadioField(label='Report Type:',default='error', choices = [('error', 'Error'), ('suggestions', 'Suggestion'), ('translation', 'Translation')],
                       validators=[DataRequired()])
    submit = SubmitField('Submit')

