from app.db import db


class PageTemplate(db.Model):
    """Page Templates for tables"""
    __tablename__ = 'page_templates'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), index=True)
    list_page = db.Column(db.String(30), nullable=True)
    list_kwargs = db.Column(db.String(120), nullable=True)
    add_page = db.Column(db.String(30), nullable=True)
    add_kwargs = db.Column(db.String(120), nullable=True)
    edit_page = db.Column(db.String(30), nullable=True)
    edit_kwargs = db.Column(db.String(120), nullable=True)
    view_page = db.Column(db.String(30), nullable=True)
    view_kwargs = db.Column(db.String(120), nullable=True)
    delete_page = db.Column(db.String(30), nullable=True)
    delete_kwargs = db.Column(db.String(120), nullable=True)

    # Relationship to tables
    table = db.relationship('Table',
                            backref=db.backref('page_templates',
                                               uselist=False, order_by=id))

    def __repr__(self):
        """Field info"""

        return f'<PageTemplate table_id={self.table_id} list={self.list_page}>'
