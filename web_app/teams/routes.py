from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from flask_user import roles_required

from web_app.teams.forms import NewTeamForm
from web_app import db

from web_app.models import User, Team

teams = Blueprint('teams', __name__)

@teams.route('/teams')
@login_required
def teamss():
    return render_template("teams.html", user=current_user, teams=Team.query.all())

@teams.route('/teams/new', methods=['GET', 'POST'])
@login_required
@roles_required(['Admin',])
def new_team():
    form = NewTeamForm()
    name = form.name.data
    description = form.description.data

    users = User.query.all()
    # for user in users:
    #     print(user, ' ', user.teams)
    checked_users = []
    if form.validate_on_submit():
        for user in users:
            id = 'user-manage-' + str(user.id)
            print(id)
            if request.form.get(id):
                print('checked')
                checked_users.append(user)
        new_team = Team(name=name, description=description)
        new_team.users = checked_users
        db.session.add(new_team)
        db.session.commit()

        # print(name, ' ', description, ' ', checked_users)
        flash('New team has been created', 'success')
        return redirect(url_for('teams.teamss'))
    return render_template("new_team.html", user=current_user, form=form, users=User.query.all())

@teams.route('/teams/<int:team_id>')
@login_required
def team(team_id):
    from datetime import datetime
    today = datetime.today()
    team = Team.query.get_or_404(team_id)
    return (render_template("team.html", user=current_user, team=team, today=today))