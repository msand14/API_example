from flask import Flask, render_template , session, redirect, url_for
from . import main
from .forms import UserForm

#Functions
@main.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',form = form, user_name = session.get('name'))