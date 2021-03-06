from typing import List
from app.db import db


class Project(db.Model):
    """Table for Project settings and information."""

    __tablename__ = 'projects'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    brand = db.Column(db.String(30))
    logo = db.Column(db.String(120))
    db_uri = db.Column(db.String(200))

    # Relationship to user
    user = db.relationship('User',
                           backref=db.backref('projects', order_by=id))

    def __repr__(self):
        """Project info"""

        return f'<Project project_id={self.id} project_name={self.name} user_id={self.user_id}>'

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
