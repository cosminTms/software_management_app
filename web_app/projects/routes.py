from math import floor

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from flask_user import roles_required

from web_app import db
from web_app.models import Project, Team, Role, User, DevelopmentPhase, TaskDescription, Task
from web_app.projects.forms import NewProjectForm, NewTaskForm, EditTask

projects = Blueprint('projects', __name__)

@projects.route('/projects', methods=['GET',])
@login_required
def projectss():
    from datetime import datetime
    today = datetime.today()
    return render_template("projects.html", user=current_user, projects=Project.query.all(), today=today)

def completed_story_points(project):
    tasks = project.tasks
    completed = 0
    total = 0

    for task in tasks:
        if task.completed:
            completed += task.story_points
        total += task.story_points
    return completed, total

@projects.route('/projects/<int:project_id>')
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    from datetime import datetime
    today = datetime.today()
    completed, total = completed_story_points(project)
    try:
        percentage = floor(completed / total * 100)
    except:
        percentage = 0
    print(completed, ' ', total, ' ', percentage)
    return (render_template("project.html", user=current_user, project=project,
                            today=today, admin=Role.query.filter_by(name='Admin').first().users[0],
                            completed=completed, total=total, percentage=percentage))


@projects.route('/projects/new', methods=['GET', 'POST'])
@login_required
@roles_required(['Admin',])
def new_project():
    form = NewProjectForm()
    name = form.name.data
    description = form.description.data
    start_date = form.start_date.data
    deadline = form.deadline.data

    managers = []
    try:
        managers = Role.query.filter_by(name='Project Manager').first().users
    except:
        managers = []
    teams = Team.query.all()
    users = User.query.all()

    checked_pms = []
    checked_teams = []
    checked_users = []

    if form.validate_on_submit():
        for pm in managers:
            id = 'pm-manage-' + str(pm.id)
            if request.form.get(id):
                checked_pms.append(pm)
        for team in teams:
            id = 'team-manage-' + str(team.id)
            if request.form.get(id):
                checked_teams.append(team)
        for user in users:
            id = 'user-manage-' + str(user.id)
            if request.form.get(id):
                checked_users.append(user)

        new_project = Project(name=name, description=description, start_date=start_date, deadline=deadline)
        new_project.managers = checked_pms
        new_project.users = checked_users
        new_project.teams = checked_teams
        new_dev_phase = DevelopmentPhase()
        new_project.phases = DevelopmentPhase()

        db.session.add(new_dev_phase)
        db.session.add(new_project)
        db.session.commit()
        print(name, ' ', description, ' ', checked_pms, ' ', checked_teams, ' ', checked_users, ' ', start_date, ' ', deadline)
        flash('New project has been created', 'success')
        return redirect(url_for('projects.projectss'))
    return render_template("new_project.html", user=current_user, form=form, users=User.query.all(),
                           teams=Team.query.all(), pms=managers)

def project_users_all(project):
    users = []
    for team in project.teams:
        for u in team.users:
            if not u in users:
                users.append(u)
    for us in project.users:
        if not us in users:
            users.append(us)

    return users


@projects.route('task/<int:proiect_id>', methods=['GET', 'POST'])
@login_required
def new_task(proiect_id):
    form = NewTaskForm()
    project = Project.query.get_or_404(proiect_id)
    users = project_users_all(project)

    title = form.title.data
    description = form.description.data
    start_date = form.start_date.data
    deadline = form.deadline.data
    story_points = form.story_points.data
    assigned_users = []

    if form.validate_on_submit():
        for user in users:
            id = 'user-manage-' + str(user.id)
            if request.form.get(id):
                assigned_users.append(user)

        new_task_description = TaskDescription(title=title, description=description)
        new_task = Task(start_date=start_date, deadline=deadline, story_points=story_points)
        new_task.users = assigned_users
        new_task.task_descriptions = [new_task_description]
        new_task.projects = [project]

        db.session.add(new_task_description)
        db.session.add(new_task)
        db.session.commit()
        print(title, ' ', description, ' ', assigned_users, ' ', start_date, ' ', deadline)
        flash('New task has been created', 'success')
        return redirect(url_for('projects.project', project_id=project.id))
    return render_template("new_task.html", user=current_user, project=project, users=users, form=form)


@projects.route('tasks/<int:task_id>', methods=['GET', 'POST'])
@login_required
def task(task_id):
    form = EditTask()
    task = Task.query.get_or_404(task_id)
    project = task.projects[0]
    users = project_users_all(project)
    assigned_users = task.users

    if form.validate_on_submit():
        task.task_descriptions[0].title = form.title.data
        task.task_descriptions[0].description = form.description.data
        task.start_date = form.start_date.data
        task.deadline = form.deadline.data
        task.story_points = form.story_points.data
        new_assigned_users = []

        for user in users:
            id = 'user-manage-' + str(user.id)
            if request.form.get(id):
                new_assigned_users.append(user)
        task.users = new_assigned_users

        if request.form.get("is_completed"):
            task.completed = True
        db.session.commit()
        flash('Task has been updated!', 'success')
        return redirect(url_for('projects.project', project_id=project.id))

    elif request.method == 'GET':
        form.title.data = task.task_descriptions[0].title
        form.description.data = task.task_descriptions[0].description
        form.start_date.data = task.start_date
        form.deadline.data = task.deadline
        form.story_points.data = task.story_points
        assigned_users = task.users
        unassigned_users = set(users) - set(assigned_users)
    return (render_template("task.html", user=current_user, form=form, project=project, task=task, assigned_users=assigned_users, unassigned_users=unassigned_users))
