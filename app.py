import os
from flask import Flask, render_template , session, abort, redirect, url_for
from flask_bootstrap import Bootstrap
from forms import UserForm

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'nothing'

bootstrap = Bootstrap(app)

#Functions
@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = UserForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('main_page'))
    return render_template('user_main.html',form = form, user_name = session.get('name'))
