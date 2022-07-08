from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""
    # Configure to use our MSSQL/PostgreSQL database

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://sa:StrongPa55#@localhost/CogenDB'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5433/CogenDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
