#import flask-wtf extension classes
#flask-wtf makes working with web forms easier
from flask_wtf.form import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, DataRequired

class NameForm(FlaskForm):
  name = StringField("What is your name?", validators=[DataRequired()])
  submit = SubmitField("Submit")
