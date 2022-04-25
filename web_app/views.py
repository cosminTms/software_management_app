from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/tasks')
@login_required
def tasks():
    tasks = current_user.tasks
    done = {}
    waiting = {}
    for task in tasks:
        project = task.projects[0]
        if task.completed:
            if project in done:
                done[project].append(task)
            else:
                done[project] = [task,]
        else:
            if project in waiting:
                waiting[project].append(task)
            else:
                waiting[project] = [task,]
    return render_template("tasks.html", waiting=waiting, done=done, user=current_user)

@views.route('/kanban')
@login_required
def kanban():
    return render_template("kanban.html", user=current_user)

@views.route('/issues')
@login_required
def issues():
    return render_template("issues.html", user=current_user)
