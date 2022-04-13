from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from web_app.forms import UpdateAccountForm
from web_app import db
import secrets
import os
from PIL import Image

views = Blueprint('views', __name__)

# users = ['dev', 'pm', 'cto']
# current_user = users[0]

@views.route('/', methods=['GET',])
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/projects', methods=['GET',])
@login_required
def projects():
    return render_template("projects.html", user=current_user)

@views.route('/teams')
@login_required
def teams():
    return render_template("teams.html", user=current_user)

@views.route('/tasks')
@login_required
def tasks():
    return render_template("tasks.html", user=current_user)

@views.route('/kanban')
@login_required
def kanban():
    return render_template("kanban.html", user=current_user)

@views.route('/issues')
@login_required
def issues():
    return render_template("issues.html", user=current_user)

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

@views.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('views.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", user=current_user, image_file=image_file, form = form)