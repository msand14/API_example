from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class UserForm(FlaskForm):
    name = StringField('Write here your username:', validators=[DataRequired()])
    submit = SubmitField('Submit')

