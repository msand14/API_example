from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    user_email    = StringField('Email:', validators=[ DataRequired(), Email(), Length(1,35)])
    user_password = PasswordField('Password:',validators=[DataRequired()])
    remember      = BooleanField('Remember me')
    submit        = SubmitField('Log in')