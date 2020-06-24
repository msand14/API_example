from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from ..models import User
from flask import current_app
class LoginForm(FlaskForm):
    user_email    = StringField('Email:', validators=[ DataRequired(), Email(), Length(1,35)])
    user_password = PasswordField('Password:',validators=[DataRequired()])
    remember      = BooleanField('Remember me')
    submit        = SubmitField('Log in')

class RegisterForm(FlaskForm):
    email     = StringField('Email', validators=[DataRequired(),Length(1,35),Email()])
    username       = StringField('Username', validators=[DataRequired(), Length(1,64),
     Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have letters, numbers dots or underscores')])
    password  = PasswordField('Password', validators=[DataRequired(),EqualTo('password2',
     message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email= field.data).first():
            raise ValidationError('Email already exists.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists.')

class RegisterFormStudent(RegisterForm):
    key = StringField('Key',validators=[DataRequired(),Length(1,64)])
    submit = SubmitField('Register')
    def validate_key(self, field):
        if field != current_app.config['KEY_STUDENT']:
            raise ValidationError('Key not valid.')

class RegisterFormTeacher(RegisterForm):
    key = StringField('Key',validators=[DataRequired(),Length(1,64)])
    submit = SubmitField('Register')
    def validate_key(self, field):
        if field != current_app.config['KEY_TEACHER']:
            raise ValidationError('Key not valid.')
