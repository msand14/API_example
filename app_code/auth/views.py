from flask import render_template,  redirect, url_for, request, flash
from . import auth
from .forms import LoginForm
from ..models import User
from flask_login import login_user, login_required, logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.user_email.data.lower()).first()
        if user is not None and user.verify_pswd(form.user_password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out!','error')
    return redirect((url_for('main.index')))