import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template , session, abort, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import UserForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
POSTGRES_URL = os.environ.get("POSTGRES_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PW = os.environ.get("POSTGRES_PW")
POSTGRES_DB =os.environ.get("POSTGRES_DB")
POSTGRES_PORT_N =os.environ.get("POSTGRES_PORT_N")

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'nothing'
app.config['SQLALCHEMY_DATABASE_URI'] = \
'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_URL}:{POSTGRES_PORT_N}/{POSTGRES_DB}' \
         .format(POSTGRES_PW = POSTGRES_PW, POSTGRES_URL =  POSTGRES_URL, POSTGRES_USER = \
             POSTGRES_USER, POSTGRES_DB=POSTGRES_DB, POSTGRES_PORT_N = POSTGRES_PORT_N )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
#DB classes

db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id    = db.Column(db.Integer, primary_key = True)
    rolename  = db.Column(db.String(64), unique= True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return 'Role %r' % self.rolename

class User(db.Model):
    __tablename__ = 'users'
    id           = db.Column(db.Integer, primary_key = True)
    role_id      = db.Column(db.Integer,db.ForeignKey('roles.id'))
    username     = db.Column(db.String(64), unique=True, index=True )
    class_number = db.Column(db.SmallInteger)

    def __repr__(self):
        return 'User %r' % self.username
    
#Functions
@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = UserForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('main_page'))
    return render_template('user_main.html',form = form, user_name = session.get('name'))
