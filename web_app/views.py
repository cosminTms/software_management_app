from flask import Blueprint, render_template
from flask_login import login_required

views = Blueprint('views', __name__)

users = ['dev', 'pm', 'cto']
current_user = users[0]

@views.route('/', methods=['GET',])
@views.route('/home')
# @login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/projects', methods=['GET',])
def projects():
    return render_template("projects.html", user=current_user)

@views.route('/teams')
def teams():
    return render_template("teams.html", user=current_user)

@views.route('/tasks')
def tasks():
    return render_template("tasks.html", user=current_user)

@views.route('/kanban')
def kanban():
    return render_template("kanban.html", user=current_user)

@views.route('/issues')
def issues():
    return render_template("issues.html", user=current_user)
