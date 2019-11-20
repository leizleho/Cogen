"""Models and database functions for this app."""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """User model. Inherits UserMixin to get access to
    is_authenticated(), is_active(), is_anonymous(), get_id() which we will
    call in our app routes.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        """User info"""
        return f'<User id={self.id} username={self.username} email={self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    """Table for Project settings and information."""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    db_uri = db.Column(db.String(200))

    # Relationship to user
    user = db.relationship('User',
                           backref=db.backref('projects', order_by=id))

    def __repr__(self):
        """Project info"""

        return f'<Project project_id={self.id} project_name={self.name} user_id={self.user_id}>'


class Table(db.Model):
    """Table info for each project."""

    __tablename__ = 'tables'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey('projects.id'), index=True)
    name = db.Column(db.String(30), nullable=False)

    # Relationship to project
    project = db.relationship('Project',
                              backref=db.backref('tables', order_by=id))

    def __repr__(self):
        """Table info"""

        return f'<Table table_id={self.id} table_name={self.name} project_id={self.project_id}>'


class Field(db.Model):
    """Fields info for each table."""

    __tablename__ = 'fields'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    table_id = db.Column(
        db.Integer, db.ForeignKey('tables.id'), index=True)
    name = db.Column(db.String(30), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    placeholder = db.Column(db.String(100))
    input_type = db.Column(db.String(30))
    required = db.Column(db.Boolean, default=False)
    list_page = db.Column(db.Boolean, default=False)
    add_page = db.Column(db.Boolean, default=False)
    edit_page = db.Column(db.Boolean, default=False)
    view_page = db.Column(db.Boolean, default=False)
    default_val = db.Column(db.String(200))
    kwargs = db.Column(db.Text)

    # Relationship to tables
    table = db.relationship('Table',
                            backref=db.backref('fields', order_by=id))

    def __repr__(self):
        """Field info"""

        return f'<Field field_id={self.id} field_name={self.name} table_id={self.table_id}>'


class PageTemplate(db.Model):
    """Page Templates for tables"""
    __tablename__ = 'page_templates'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    table_id = db.Column(
        db.Integer, db.ForeignKey('tables.id'), index=True)
    page = db.Column(db.String(30), nullable=False)
    template = db.Column(db.String(30), nullable=True)
    kwargs = db.Column(db.String(30), nullable=True)

    # Relationship to tables
    table = db.relationship('Table',
                            backref=db.backref('page_templates', order_by=id))

    def __repr__(self):
        """Field info"""

        return f'<PageTemplate template={self.template} table_id={self.table_id}>'


# Additional Features if time allows
# class Relationship(db.Model):
#     """Table Relationships"""

#     __tablename__ = "relationships"

#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     project_id = db.Column(
#         db.Integer, db.ForeignKey('projects.id'), index=True)
#     parent_table = db.Column(db.String(30))
#     parent_key = db.Column(db.String(30))
#     child_table = db.Column(db.String(30))
#     child_key = db.Column(db.String(30))

#     # Relationship to projects
#     project = db.relationship('Project',
#                               backref=db.backref('relationships', order_by=id))

#     def __repr__(self):
#         """Field info"""

#         return f'<Relationship relationship_id={self.id}  project_id={self.project_id}>'


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""
    # Configure to use our PostgreSQL database

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5433/testdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
