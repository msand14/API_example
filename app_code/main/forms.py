from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    name = StringField('Write here your username:', validators=[DataRequired()])
    submit = SubmitField('Submit')