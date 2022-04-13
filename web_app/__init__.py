from os import path
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "e0421cdfcb8e733acdcf876d782b3061ad0b2d24929009465ff91f6904cdfb6a"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['USER_ENABLE_EMAIL'] = False


    db.init_app(app)

    from web_app.views import views
    from web_app.auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from web_app.models import User

    create_database(app)

    # Setup Flask-User
    user_manager = UserManager(app, db, User)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    from web_app.models import Role

    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')