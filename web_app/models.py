from flask_user import UserMixin

from web_app import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    joined_at = db.Column(db.DateTime(), default=datetime.now)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # User fields
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # Relationships
    roles = db.relationship('Role', secondary='user_roles', back_populates="users")
    teams = db.relationship('Team', secondary='team_members', back_populates="users")
    projects = db.relationship('Project', secondary='project_members', back_populates="users")
    tasks = db.relationship('Task', secondary='user_tasks', back_populates="users")
    managed_projects = db.relationship('Project', secondary='project_managers', back_populates="managers")

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

    def get_id(self):
        return str(self.id)


class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    users = db.relationship('User', secondary='user_roles', back_populates="roles")

    def __repr__(self):
        return f"Role('{self.name}')"


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Team(db.Model):
    __tablename__ = 'teams'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime(), default=datetime.now)

    # Relationships
    users = db.relationship('User', secondary='team_members', back_populates="teams")
    projects = db.relationship('Project', secondary='project_teams', back_populates="teams")

    def __repr__(self):
        return f"Team('{self.name}')"


class TeamMembers(db.Model):
    __tablename__ = 'team_members'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))


class ProjectMembers(db.Model):
    __tablename__ = 'project_members'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id', ondelete='CASCADE'))


class ProjectTeams(db.Model):
    __tablename__ = 'project_teams'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    team_id = db.Column(db.Integer(), db.ForeignKey('teams.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id', ondelete='CASCADE'))
    # added_at = db.Column(db.DateTime, default=datetime.utcnow)


class DevelopmentPhase(db.Model):
    __tablename__ = 'development_phases'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    concept = db.Column(db.Boolean, default=True)
    inception = db.Column(db.Boolean, default=False)
    iterations = db.Column(db.Integer(), default=0)
    requirements = db.Column(db.Boolean(), default=False)
    development = db.Column(db.Boolean(), default=False)
    testing = db.Column(db.Boolean(), default=False)
    deliver = db.Column(db.Boolean(), default=False)
    feedback = db.Column(db.Boolean(), default=False)
    release = db.Column(db.Boolean(), default=False)
    maintenance = db.Column(db.Boolean(), default=False)
    retirement = db.Column(db.Boolean(), default=False)

    projects = db.relationship('Project', secondary='project_phases', back_populates="development_phases")


class ProjectManagers(db.Model):
    __tablename__ = 'project_managers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id', ondelete='CASCADE'))


class ProjectPhases(db.Model):
    __tablename__ = 'project_phases'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    phase_id = db.Column(db.Integer(), db.ForeignKey('development_phases.id', ondelete='CASCADE'))
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id', ondelete='CASCADE'))


class Project(db.Model):
    __tablename__ = 'projects'
    __table_args__ = {'extend_existing': True}
    # Project Concept Information
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)

    # Project Human Resources
    managers = db.relationship('User', secondary='project_managers', back_populates="managed_projects")
    teams = db.relationship('Team', secondary='project_teams', back_populates="projects")
    users = db.relationship('User', secondary='project_members', back_populates="projects")
    tasks = db.relationship('Task', secondary='project_tasks', back_populates="projects")

    # Project Backlog + Sprint Backlogs
    sprints = db.relationship('Sprint', secondary='project_sprints', back_populates="projects")

    # Project Current Development Phase ['Concept', 'Inception', 'Iterations': ['Req', 'Dev', 'Testing', 'Deliver', 'Feedback'], 'Release', 'Maintenance', 'Retirement']
    development_phases = db.relationship('DevelopmentPhase', secondary='project_phases', back_populates="projects")

    # Project Log

    def __repr__(self):
        return f"Project('{self.name}')"


class TaskDescription(db.Model):
    __tablename__ = 'task_descriptions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    tasks = db.relationship('Task', secondary='task_task_descriptions', back_populates="task_descriptions")

    def __repr__(self):
        return f"Task('{self.title}')"


class Task(db.Model):
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    story_points = db.Column(db.Integer, default=0)

    task_descriptions = db.relationship('TaskDescription', secondary='task_task_descriptions', back_populates="tasks")
    users = db.relationship('User', secondary='user_tasks', back_populates="tasks")
    sprints = db.relationship('Sprint', secondary='sprint_tasks', back_populates="tasks")
    projects = db.relationship('Project', secondary='project_tasks', back_populates="tasks")


class Sprint(db.Model):
    __tablename__ = 'sprints'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    deadline = db.Column(db.DateTime, nullable=False)

    tasks = db.relationship('Task', secondary='sprint_tasks', back_populates="sprints")
    projects = db.relationship('Project', secondary='project_sprints', back_populates="sprints")

    def __repr__(self):
        return f"Sprint ('{self.iteration}')"


class SprintTasks(db.Model):
    __tablename__ = 'sprint_tasks'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    sprint_id = db.Column(db.Integer(), db.ForeignKey('sprints.id', ondelete='CASCADE'))
    task_id = db.Column(db.Integer(), db.ForeignKey('tasks.id', ondelete='CASCADE'))


class UserTasks(db.Model):
    __tablename__ = 'user_tasks'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    task_id = db.Column(db.Integer(), db.ForeignKey('tasks.id', ondelete='CASCADE'))


class ProjectTasks(db.Model):
    __tablename__ = 'project_tasks'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id', ondelete='CASCADE'))
    task_id = db.Column(db.Integer(), db.ForeignKey('tasks.id', ondelete='CASCADE'))


class ProjectSprints(db.Model):
    __tablename__ = 'project_sprints'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    project_id = db.Column(db.Integer(), db.ForeignKey('projects.id', ondelete='CASCADE'))
    sprint_id = db.Column(db.Integer(), db.ForeignKey('sprints.id', ondelete='CASCADE'))


class TaskTaskDescriptions(db.Model):
    __tablename__ = 'task_task_descriptions'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer(), primary_key=True)
    task_id = db.Column(db.Integer(), db.ForeignKey('tasks.id', ondelete='CASCADE'))
    task_description_id = db.Column(db.Integer(), db.ForeignKey('task_descriptions.id', ondelete='CASCADE'))
