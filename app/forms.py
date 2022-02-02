# Forms

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class EntryForm(FlaskForm):
    name = StringField('Enter Pokemon Name', validators=[DataRequired()])
    submit = SubmitField('Submit')