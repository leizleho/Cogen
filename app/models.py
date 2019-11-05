"""Models and database functions for this app."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User of Cogen App."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return f"<User id={self.id} email={self.email}>"


class Project(db.Model):
    """Table for Project settings and information."""

    __tablename__ = "projects"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    db_uri = db.Column(db.String(200))

    # Relationship to user
    user = db.relationship("User",
                           backref=db.backref("projects", order_by=id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Project project_id={self.id} user_id={self.user_id}>"""


##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5433/testdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")
