from flask import Blueprint, render_template, url_for, flash, redirect, request, session
from flask_login import login_required, current_user

from web_app.main.forms import UpdateAccountForm
from web_app import db
import secrets
import os
from PIL import Image

main = Blueprint('main', __name__)

@main.route('/', methods=['GET',])
@main.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

def save_picture(form_picture):
    from main import app
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename

@main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    # print('entered /account')
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # print('entered /account -> post')
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        print(current_user.username, ' ', form.username.data)

        db.session.commit()
        # print('Changes commited')
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        # print('entered /account -> get')
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", user=current_user, image_file=image_file, form = form)