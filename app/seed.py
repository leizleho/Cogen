from models import db, connect_to_db, User, Project, Table, Field, PageTemplate


def users_data():
    """Create some sample data."""
    User.query.delete()

    u1 = User(id=1, fname='Leizle', lname='Ho', username='leizleho',
              email='leizleho@yahoo.com')
    u1.set_password('12345')

    u2 = User(id=2, fname='Rain', lname='Ulan', username='rain',
              email='rain.ulan@gmail.com')
    u2.set_password('12345')
    db.session.add_all([u1, u2])
    db.session.commit()


def projects_data():
    Project.query.delete()
    p1 = Project(id=1, user_id=1, name='tgallery', description='Gallery of Travel Photos',
                 db_uri="postgresql://postgres@localhost:5433/testdb")
    p2 = Project(id=2, user_id=1, name='jobapptracker', description='Job Application Tracker',
                 db_uri="postgresql://postgres@localhost:5433/testdb2")
    p3 = Project(id=3, user_id=1, name='rfq', description='Web Dev Services - Request for Quote',
                 db_uri="postgresql://postgres@localhost:5433/testdb3")
    db.session.add_all([p1, p2, p3])
    db.session.commit()


def tables_data():
    Table.query.delete()
    t1 = Table(id=1, project_id=1, name='photos')
    t2 = Table(id=2, project_id=1, name='albums')
    t3 = Table(id=3, project_id=1, name='album_contents')
    db.session.add_all([t1, t2, t3])
    db.session.commit()


def fields_data():
    Field.query.delete()
    f1 = Field(id=1, table_id=1, name='photo', label='Photo', placeholder='Photo', input_type='File',
               required=True, list_page=False, add_page=True, edit_page=True, view_page=True)

    f2 = Field(id=2, table_id=1, name='caption', label='Caption', placeholder='Caption', input_type='String',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f3 = Field(id=3, table_id=1, name='date_taken', label='Date', placeholder='Date', input_type='DateTime',
               required=False, list_page=True, add_page=True, edit_page=True, view_page=True)

    f4 = Field(id=4, table_id=1, name='location', label='Location', placeholder='Location', input_type='String',
               required=False, list_page=True, add_page=True, edit_page=True, view_page=True)

    f5 = Field(id=5, table_id=2, name='name', label='Album Name', placeholder='Album Name', input_type='String',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f6 = Field(id=6, table_id=2, name='description', label='Description', placeholder='Description', input_type='String',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f7 = Field(id=7, table_id=3, name='album_id', label='Album', placeholder='Album', input_type='Integer',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    f8 = Field(id=8, table_id=3, name='photo_id', label='Photo', placeholder='Photo', input_type='Integer',
               required=True, list_page=True, add_page=True, edit_page=True, view_page=True)

    db.session.add_all([f1, f2, f3, f4, f5, f6, f7, f8])
    db.session.commit()


def template_data():
    PageTemplate.query.delete()
    m1 = PageTemplate(id=1, table_id=1, page='list', template='card')
    db.session.add(m1)
    db.session.commit()


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print("Connected to DB.")
