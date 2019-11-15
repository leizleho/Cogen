from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length


class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[
        InputRequired("Project name is required"), Length(min=3, max=20, message="Project name must have length between 3 to 20")])
    description = TextAreaField('Project description', validators=[
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
    input_type = SelectField('Input type', choices=[('String', 'text'),
                                                    ('Boolean', 'checkbox'),
                                                    ('DateTime', 'datetime'),
                                                    ('Email', 'email'),
                                                    ('File', 'file'),
                                                    ('String', 'image'),
                                                    ('Hidden', 'hidden'),
                                                    ('Password', 'password'),
                                                    ('Integer', 'number'),
                                                    ('Radio', 'radio'),
                                                    ('Select', 'select'),
                                                    ('Text', 'textarea'),
                                                    ('Url', 'url')
                                                    ])
    required = BooleanField(u'Required', default='checked',
                            render_kw={'checked': True})
    list_page = BooleanField('List',
                             false_values=(False, 'f', 0))
    add_page = BooleanField('Add', false_values=(False, 'f', 0))
    edit_page = BooleanField('Edit',
                             false_values=(False, 'f', 0))
    view_page = BooleanField('View',
                             false_values=(False, 'f', 0))
    default_val = StringField('Default value')
    kwargs = TextAreaField('Keyword arguments')
