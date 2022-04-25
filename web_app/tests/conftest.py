import datetime

import pytest
from flask_login import FlaskLoginClient
from werkzeug.security import generate_password_hash

from web_app import create_app, db
from web_app.models import User, Role, Team, Project


@pytest.fixture()
def new_user():
    user = User(email='johnSmith@email.com', password=generate_password_hash('password', method='sha256'),
                first_name='John', last_name='Smith', username='john', roles=[Role(name='Developer')])
    return user

@pytest.fixture()
def admin_user():
    user = User(email='johnSmith@email.com', password=generate_password_hash('password', method='sha256'),
                first_name='John', last_name='Smith', username='john', roles=[Role(name='Admin')])
    return user

@pytest.fixture()
def developer_user():
    user = User(email='johnSmith@email.com', password=generate_password_hash('password', method='sha256'),
                first_name='John', last_name='Smith', username='john', roles=[Role(name='Developer')])
    return user

@pytest.fixture()
def pm_user():
    user = User(email='johnSmith@email.com', password=generate_password_hash('password', method='sha256'),
                first_name='John', last_name='Smith', username='john', roles=[Role(name='Project Manager')])
    return user

@pytest.fixture()
def cto_user():
    user = User(email='johnSmith@email.com', password=generate_password_hash('password', method='sha256'),
                first_name='John', last_name='Smith', username='john', roles=[Role(name='CTO')])
    return user

@pytest.fixture()
def new_team():
    team = Team(name='Team One', description='Team One Description')
    return team


@pytest.fixture()
def new_project():
    project = Project(name='Project One', description='Project One Description', start_date=datetime.date(2022,5,4), deadline = datetime.date(2022, 6, 10))
    return project


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    app.test_client_class = FlaskLoginClient

    # other setup can go here
    with app.app_context():
        db.create_all()
        admin = User(first_name="admin", last_name="admin", username='admin',
                     email='admin@email.com', password=generate_password_hash('123', method='sha256'),
                     roles=[Role(name='Admin')])
        josh = User(first_name="josh", last_name="smith", username='josh',
                     email='josh@email.com', password=generate_password_hash('123', method='sha256'),
                     roles=[Role(name='Developer')])
        team_one = Team(name='Team One', description='Team One Description')
        team_one.users = [josh,]
        project_one = Project(name='Project One', description='Project One Description', deadline = datetime.date(2022, 6, 10))

        db.session.add(admin)
        db.session.add(josh)
        db.session.add(team_one)
        db.session.add(project_one)
        db.session.commit()

        yield app

        # clean up / reset resources here
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def logged_client(app):
    user = User.query.get(1)
    return app.test_client(user=user)


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

