from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[
        InputRequired("Project name is required"), Length(min=3, max=20, message="Project name must have length between 3 to 20")])
    description = StringField('Project description', validators=[
        InputRequired("Project description is required"), Length(min=20, max=200, message="Project Description must have length between 20 to 200")])
    db_uri = StringField('Database Connection String')
