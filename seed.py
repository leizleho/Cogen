from app.db import db, connect_to_db
from app.models.user import User
from app.models.project import Project
from app.models.table import Table
from app.models.field import Field
from app.models.pagetemplate import PageTemplate


def seed_data():
    db.create_all()
    users_data()
    projects_data()
    tables_data()
    fields_data()
    template_data()


def users_data():
    """Create some sample data."""
    User.query.delete()

    u1 = User(fname='Leizle', lname='Ho', username='leizleho',
              email='leizleho@yahoo.com')
    u1.set_password('12345')

    u2 = User(fname='Higor', lname='Vaz', username='higorvaz',
              email='higorvaz@gmail.com')
    u2.set_password('12345')
    db.session.add_all([u1, u2])
    db.session.commit()


def projects_data():
    Project.query.delete()
    p1 = Project(user_id=2, name='tgallery', description='Gallery of Travel Photos',
                 db_uri="mssql+pymssql://sa:StrongPa55#@localhost/CogenDBGallery")
                #  db_uri="postgresql://postgres@localhost:5433/CogenDB")
    # p2 = Project(user_id=1, name='jobapptracker', description='Job Application Tracker',
    #              db_uri="postgresql://postgres@localhost:5433/testdb2")
    # p3 = Project(user_id=1, name='rfq', description='Web Dev Services - Request for Quote',
    #              db_uri="postgresql://postgres@localhost:5433/testdb3")
    # db.session.add_all([p1, p2, p3])
    db.session.add_all([p1])
    db.session.commit()


def tables_data():
    Table.query.delete()
    t1 = Table(project_id=1, name='photos')
    t2 = Table(project_id=1, name='albums')
    t3 = Table(project_id=1, name='album_contents')
    db.session.add_all([t1, t2, t3])
    db.session.commit()


def fields_data():
    Field.query.delete()
    f1 = Field(table_id=1, name='photo', label='Photo', placeholder='Photo', input_type='image',
               required=True, list_page=False, add_page=True, edit_page=True, view_page=True)

    f2 = Field(table_id=1, name='caption', label='Caption', placeholder='Caption', input_type='text',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f3 = Field(table_id=1, name='date_taken', label='Date', placeholder='Date', input_type='datetime',
               required=False, list_page=True, add_page=True, edit_page=True, view_page=True)

    f4 = Field(table_id=1, name='location', label='Location', placeholder='Location', input_type='text',
               required=False, list_page=True, add_page=True, edit_page=True, view_page=True)

    f5 = Field(table_id=2, name='name', label='Album Name', placeholder='Album Name', input_type='text',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f6 = Field(table_id=2, name='description', label='Description', placeholder='Description', input_type='text',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f7 = Field(table_id=3, name='album_id', label='Album', placeholder='Album', input_type='number',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f8 = Field(table_id=3, name='photo_id', label='Photo', placeholder='Photo', input_type='number',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8])
    db.session.commit()


def template_data():
    PageTemplate.query.delete()
    m1 = PageTemplate(table_id=1, list_page='card',
                      list_kwargs='title=caption,img=photo',
                      add_page='default',
                      edit_page='default',
                      view_page='default',
                      delete_page='default')
    db.session.add(m1)
    db.session.commit()


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
