from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from web_app.models import Team

class NewTeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Team')

    def validate_name(self, name):
        name = Team.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('Team name already exists!')