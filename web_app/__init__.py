from os import path
from flask import Flask, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager
from werkzeug.security import generate_password_hash
from web_app.config import Config

db = SQLAlchemy()
DB_NAME = "database.db"

# Application factory => can then create multiple instances of this app later
# Good for:
#   1.Testing. You can have instances of the application with different settings to test every case
#   2.Multiple instances. Can run different versions of the same application
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from web_app.views import views
    from web_app.auth import auth
    from web_app.main.routes import main
    from web_app.teams.routes import teams
    from web_app.projects.routes import projects

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(teams, url_prefix='/')
    app.register_blueprint(projects, url_prefix='/')

    from web_app.models import User, Role, Team, Project

    create_database(app)

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        print('session id: ',session["_user_id"])
        return User.query.get(int(id))

    # create_users()

    admin = Admin(app, name='Technologist.io', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(ModelView(Team, db.session))
    admin.add_view(ModelView(Project, db.session))

    return app

def create_database(app):
    from web_app.models import Role

    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def create_users():
    from web_app.models import User
    users = {
        "user1":{
            "first_name": "John",
            "last_name": "Smith",
            "role": "Developer",
            "username": "johnSmith",
            "email": "johnSmith@email.com",
            "password": "123"
        },
        "user2":{
            "first_name": "Walter",
            "last_name": "Kaye",
            "role": "Developer",
            "username": "walterKaye",
            "email": "walterKaye@email.com",
            "password": "123"
        },
        "user3":{
            "first_name": "Joel",
            "last_name": "Antony",
            "role": "Developer",
            "username": "joelAntony",
            "email": "joelAntony@email.com",
            "password": "123"
        },
        "user4":{
            "first_name": "Katty",
            "last_name": "Finn",
            "role": "Developer",
            "username": "kattyFinn",
            "email": "kattyFinn@email.com",
            "password": "123"
        },
        "user5":{
            "first_name": "Jenae",
            "last_name": "Kimber",
            "role": "Developer",
            "username": "jenaeKimber",
            "email": "jenaeKimber@email.com",
            "password": "123"
        },
        "user6":{
            "first_name": "Bailee",
            "last_name": "Jensen",
            "role": "Developer",
            "username": "baileeJensen",
            "email": "baileeJensen@email.com",
            "password": "123"
        },
        "user7":{
            "first_name": "Tyrell",
            "last_name": "Everly",
            "role": "Developer",
            "username": "tyrellEverly",
            "email": "tyrellEverly@email.com",
            "password": "123"
        },
        "user8":{
            "first_name": "Tim",
            "last_name": "Doyle",
            "role": "Developer",
            "username": "timDoyle",
            "email": "timDoyle@email.com",
            "password": "123"
        },
        "user9":{
            "first_name": "Todd",
            "last_name": "Gervase",
            "role": "Developer",
            "username": "toddGervase",
            "email": "toddGervase@email.com",
            "password": "123"
        },
        "user10":{
            "first_name": "Frank",
            "last_name": "Carter",
            "role": "Developer",
            "username": "frankCarter",
            "email": "frankCarter@email.com",
            "password": "123"
        },
    }
    for user, value in users.items():
        first_name = value['first_name']
        last_name = value['last_name']
        roles = [value['role']]
        username = value['username']
        email = value['email']
        password = value['password']
        new_user = User(first_name=first_name, last_name=last_name, email=email, username=username,
                        roles=roles, password=generate_password_hash(password, method='sha256'))
        print(new_user)
        db.session.add(new_user)
        db.session.commit()

