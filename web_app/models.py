from flask_login import UserMixin
from web_app import db
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    team = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    members = db.relationship('User')
    project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return f"Post('{self.name}')"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_started = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    teams = db.relationship('Team')

    def __repr__(self):
        return f"Post('{self.name}','{self.date_started}')"
