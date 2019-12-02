from app.db import db


class Relationship(db.Model):
    """Table Relationships"""

    __tablename__ = "relationships"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), index=True)
    rel_type = db.Column(db.String(15))
    rel_name = db.Column(db.String(30))
    parent_table = db.Column(db.String(30))
    child_table = db.Column(db.String(30))

    # Relationship to projects
    table = db.relationship('Table',
                            backref=db.backref('relationships', order_by=id))

    def __repr__(self):
        """Relationships info"""

        return f'<Relationship relationship_id={self.id}  rel_type={self.rel_type}>'

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
