from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, StringField, TextAreaField, SubmitField,RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
try:
    from appdirs import unicode
except ImportError:
    print (ImportError)




class WordSuggestionForm(FlaskForm):
    report = TextAreaField('Report', validators=[DataRequired(),Length(min=20, max=300)])

    TYPE = RadioField(label='Report Type:',default='Suggestion',
                      choices = [('Suggestion', 'Suggestion'), ('Translation', 'Translation'),('Error', 'Error')],
                       validators=[DataRequired()])
    submit = SubmitField('Submit')

class WordSuggestionForm2(FlaskForm):
    report = TextAreaField('Report', validators=[DataRequired(),Length(min=20, max=300)])

    TYPE = RadioField(label='Report Type:',default='Add Word',
                      choices = [('Suggestion', 'Suggestion'), ('Add Word', 'Add Word'),('Error', 'Error')],
                       validators=[DataRequired()])
    submit = SubmitField('Submit')






