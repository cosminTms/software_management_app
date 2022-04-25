from flask import Blueprint, render_template, flash, redirect, url_for, session
from flask_login import login_user, current_user, logout_user, login_required
from flask_user import roles_required
from web_app.forms import RegistrationForm, LoginForm
from web_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from web_app.models import User, Role

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
@roles_required(['Admin',])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        firstName = form.first_name.data
        lastName = form.last_name.data
        password1 = form.password.data
        password2 = form.confirm_password.data

        if password1 != password2:
            flash('Passwords don\'t match', category='error')
        else:
            user_role = Role.query.filter_by(name=role).first()
            if not user_role:
                user_role = Role(name=role)
                db.session.add(user_role)
                db.session.commit()

            new_user = User(username=username, email=email, first_name=firstName, last_name=lastName,
                            password=generate_password_hash(password1, method='sha256'))
            new_user.roles = [user_role,]
            db.session.add(new_user)
            db.session.commit()

            flash('Account created!', category='success')
            return redirect(url_for('auth.register'))
    return render_template('register.html', form=form, user=current_user)

@auth.route('/login', methods=['GET','POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('views.home'))
    # print('session id: ', session["_user_id"])
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        print(user)
        print(user.id)
        print('user.get_id(): ', user.get_id())
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                print('session id: ', session["_user_id"])
                return redirect(url_for('main.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist!', category='error')
    # return render_template('login.html', form=form)
    return render_template('login.html', form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))