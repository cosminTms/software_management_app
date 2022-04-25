from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from web_app.models import Team


class NewProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date',validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])

    submit = SubmitField('Create Project')

    def validate_name(self, name):
        name = Team.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('Team name already exists!')

class NewTaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date',validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    story_points = StringField('Story Points', validators=[DataRequired(),])

    submit = SubmitField('Create Task')

    def validate_story_points(self, story_points):
        if not story_points.data.isnumeric():
            raise ValidationError('Story points value is not a positive integer!')

class EditTask(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), ])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    story_points = StringField('Story Points', validators=[DataRequired(), ])

    submit = SubmitField('Save Task')

    def validate_story_points(self, story_points):
        if not story_points.data.isnumeric():
            raise ValidationError('Story points value is not a positive integer!')