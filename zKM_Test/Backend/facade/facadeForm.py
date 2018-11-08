from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class AdditionalForm(FlaskForm):
    age = StringField('Age', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male','Male'),('Female','Female')], validators=[DataRequired()])
   # country = StringField('Country', validators=[DataRequired()])
    confirm_password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Proceed')