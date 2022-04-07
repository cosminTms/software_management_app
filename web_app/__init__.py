from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "e0421cdfcb8e733acdcf876d782b3061ad0b2d24929009465ff91f6904cdfb6a"

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app