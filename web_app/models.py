from flask_user import UserMixin

from web_app import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    joined_at = db.Column(db.DateTime(), default=datetime.now)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # User fields
    active = db.Column(db.Boolean())
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # Relationships
    roles = db.relationship('Role', secondary='user_roles')
    # team = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

# class Team(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     members = db.relationship('User')
#     project = db.Column(db.Integer, db.ForeignKey('project.id'))
#
#     def __repr__(self):
#         return f"Post('{self.name}')"
#
# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     date_started = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     description = db.Column(db.Text, nullable=False)
#     teams = db.relationship('Team')
#
#     def __repr__(self):
#         return f"Post('{self.name}','{self.date_started}')"
