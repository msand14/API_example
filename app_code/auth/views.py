from flask import render_template,  redirect, url_for, request, flash
from . import auth
from .forms import LoginForm, RegisterForm
from ..models import User
from ..models import db
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

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                email = form.email.data,
                password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('The register was succesfull. Now you can log in with your credentials.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form = form)
