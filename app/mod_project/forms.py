from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, IntegerField, BooleanField, SelectField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_login import current_user, login_required
from flask_wtf.file import FileField, FileAllowed


class ProjectForm(FlaskForm):
    name = StringField('Project name', validators=[
        InputRequired("Project name is required"), Length(min=3, max=20, message="Project name must have length between 3 to 20")])
    description = TextAreaField('Project description', validators=[
        InputRequired("Project description is required")])
    brand = StringField('Brand Name')
    logo = FileField('Logo')
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
    required = BooleanField(u'Required', default='checked')
    list_page = BooleanField('List', default='checked',
                             false_values=(False, 'f', 0))
    add_page = BooleanField('Add', default='checked',
                            false_values=(False, 'f', 0))
    edit_page = BooleanField('Edit', default='checked',
                             false_values=(False, 'f', 0))
    view_page = BooleanField('View', default='checked',
                             false_values=(False, 'f', 0))
    default_val = StringField('Default value')
    foreign_key = StringField(
        'Foreign Key (format: table_name.key_field, e.g. employees.id)')
    kwargs = TextAreaField('Keyword arguments')
    submit = SubmitField('Submit')


class PageTemplateForm(FlaskForm):
    table_id = IntegerField('Table')
    list_page = StringField('List Page Template')
    list_kwargs = TextAreaField('Keyword arguments')
    add_page = StringField('Add Page Template')
    add_kwargs = TextAreaField('Keyword arguments')
    edit_page = StringField('Edit Page Template')
    edit_kwargs = TextAreaField('Keyword arguments')
    view_page = StringField('View Page Template')
    view_kwargs = TextAreaField('Keyword arguments')
    delete_page = StringField('Delete Page Template')
    delete_kwargs = TextAreaField('Keyword arguments')
    submit = SubmitField('Submit')


class RelationshipForm(FlaskForm):
    table_id = IntegerField('Table ID')

    rel_type = SelectField('Relationship type', choices=[
                           ('one_to_one', 'One to One'),
                           ('one_to_many', 'One to Many')])
    rel_name = StringField('Name')
    parent_table = StringField('Parent Table')
    child_table = SelectField('Add relationship to', choices=[], coerce='str')

    submit = SubmitField('Submit')
