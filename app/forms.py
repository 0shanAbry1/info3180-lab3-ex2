"""Form Classes"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email

# Contact Form
class ContactForm(FlaskForm):
    clientName = StringField('Name', validators=[InputRequired()])
    clientEmail = StringField('Email', validators=[InputRequired(), Email()])
    clientSubject = StringField('Subject', validators=[InputRequired()])
    clientMessage = TextAreaField('Message', validators=[InputRequired()])
