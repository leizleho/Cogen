"""Models and database functions for this app."""
from typing import List
from app.db import db


class Table(db.Model):
    """Table info for each project."""

    __tablename__ = 'tables'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey('projects.id'), nullable=False, index=True)
    name = db.Column(db.String(30), nullable=False)

    # Relationship to project
    project = db.relationship('Project',
                              backref=db.backref('tables', order_by=id))

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

    def __repr__(self):
        """Table info"""

        return f'<Table table_id={self.id} table_name={self.name} project_id={self.project_id}>'
