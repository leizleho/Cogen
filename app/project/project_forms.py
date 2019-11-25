from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, IntegerField, BooleanField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length


class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[
        InputRequired("Project name is required"), Length(min=3, max=20, message="Project name must have length between 3 to 20")])
    description = TextAreaField('Project description', validators=[
        InputRequired("Project description is required"), Length(min=20, max=200, message="Project Description must have length between 20 to 200")])
    db_uri = StringField('Database Connection String',
                         default='postgresql://postgres@localhost:5432/testdb')
    submit = SubmitField('Submit')


class TableForm(FlaskForm):
    project_id = IntegerField('Project #')
    name = StringField('Table name', validators=[Length(
        min=2, max=30, message="Table name must have length between 2 to 30.")])
    submit = SubmitField('Submit')


class FieldForm(FlaskForm):
    table_id = IntegerField('Table #')
    name = StringField('Field name', validators=[
                       InputRequired("Field name is required")])
    label = StringField('Label', validators=[
                        InputRequired("Label is required")])
    placeholder = StringField('Placeholder', validators=[Length(
        max=30, message="Placeholder should not exceed 100.")])
    input_type = SelectField('Input type', choices=[('text', 'String'),
                                                    ('checkbox', 'Boolean'),
                                                    ('datetime', 'DateTime'),
                                                    ('email', 'Email'),
                                                    ('file', 'File'),
                                                    ('hidden', 'Hidden'),
                                                    ('image', 'Image'),
                                                    ('number', 'Integer'),
                                                    ('password', 'Password'),
                                                    ('radio', 'Radio'),
                                                    ('select', 'Select'),
                                                    ('textarea', 'Text'),
                                                    ('url', 'Url')])
    required = BooleanField(u'Required', default='checked',
                            render_kw={'checked': True})
    list_page = BooleanField('List', default='checked',
                             false_values=(False, 'f', 0))
    add_page = BooleanField('Add', default='checked',
                            false_values=(False, 'f', 0))
    edit_page = BooleanField('Edit', default='checked',
                             false_values=(False, 'f', 0))
    view_page = BooleanField('View', default='checked',
                             false_values=(False, 'f', 0))
    default_val = StringField('Default value')
    kwargs = TextAreaField('Keyword arguments')
    submit = SubmitField('Submit')
