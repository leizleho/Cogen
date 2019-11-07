from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, Length


class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[
        InputRequired("Project name is required"), Length(min=3, max=20, message="Project name must have length between 3 to 20")])
    description = StringField('Project description', validators=[
        InputRequired("Project description is required"), Length(min=20, max=200, message="Project Description must have length between 20 to 200")])
    db_uri = StringField('Database Connection String')


class TableForm(FlaskForm):
    project_id = IntegerField('Project #')
    name = StringField('Table name', validators=[Length(
        min=2, max=30, message="Table name must have length between 2 to 30.")])


class FieldForm(FlaskForm):
    table_id = IntegerField('Table #')
    name = StringField('Field name', validators=[
                       InputRequired("Field name is required")])
    label = StringField('Label', validators=[
                        InputRequired("Label is required")])
    placeholder = StringField('Placeholder', validators=[Length(
        max=30, message="Placeholder should not exceed 100.")])
    input_type = "25"
    required = BooleanField('Required?')
    list_page = BooleanField('List')
    add_page = BooleanField('Add')
    edit_page = BooleanField('Edit')
    view_page = BooleanField('View')
    string_len = IntegerField('Max char')
    default_val = StringField('Default value')
