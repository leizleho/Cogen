from app.db import db


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
    foreign_key = db.Column(db.String(65))
    kwargs = db.Column(db.Text)

    # Relationship to tables
    table = db.relationship('Table',
                            backref=db.backref('fields', order_by=id))

    def __repr__(self):
        """Field info"""

        return f'<Field field_id={self.id} field_name={self.name} table_id={self.table_id}>'
