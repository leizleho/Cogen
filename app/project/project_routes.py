"""Routes for projects"""
from flask import Blueprint, render_template, request, flash, redirect, session
from flask_login import current_user, login_required
from app.models import connect_to_db, db, User, Project, Table, Field
from app.project.project_forms import ProjectForm, TableForm, FieldForm

# Blueprint Config
project_bp = Blueprint('project_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       url_prefix='/projects')

#################### ROUTES FOR PROJECTS ######################
@project_bp.route('/', methods=['GET'])
@login_required
def show_projects():
    user_id = session["user_id"]
    projects = Project.query.filter_by(user_id=user_id).all()

    return render_template('projects.html',
                           title='Projects',
                           projects=projects)


@project_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        # Get form data
        user_id = current_user.id
        name = request.form["name"]
        description = request.form["description"]
        db_uri = request.form["db_uri"]

        new_project = Project(user_id=user_id, name=name,
                              description=description, db_uri=db_uri)

        db.session.add(new_project)
        db.session.commit()
        flash(f"Project {name} has been created.")
        return redirect(f"/projects/{new_project.id}")

    return render_template('project_create.html', title="Create Project", form=project_form)


@project_bp.route('/update/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get(project_id)
    form = ProjectForm()

    if form.validate_on_submit():
        project.name = request.form['name']
        project.description = request.form['description']
        project.db_uri = request.form['db_uri']
        db.session.commit()
        return redirect(f"/projects/{project_id}")

    form.name.data = project.name
    form.description.data = project.description
    form.db_uri.data = project.db_uri
    return render_template('project_update.html',
                           title='Projects', id=project_id, form=form)

# delete project
@project_bp.route('/del/<int:project_id>', methods=['GET', 'POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get(project_id)
    tables = Table.query.filter(Table.project_id == project.id).all()

    if request.method == 'GET':
        return render_template('project_delete.html', project=project)

    if request.method == 'POST':
        for table in tables:
            fields = Field.query.filter(Field.table_id == table.id).delete()

        tables = Table.query.filter(Table.project_id == project.id).delete()
        db.session.delete(project)
        db.session.commit()
        return redirect("/projects")


# show_project_details
@project_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def show_project_details(project_id):
    project = Project.query.get(project_id)
    return render_template("project_details.html", title="Project Info", project=project)


#################### ROUTES FOR TABLES ######################

# Create Table
@project_bp.route('/<int:project_id>/tables/create', methods=['GET', 'POST'])
@login_required
def create_table(project_id):
    table_form = TableForm()

    if table_form.validate_on_submit():
        name = request.form['name']
        new_table = Table(project_id=project_id, name=name)
        db.session.add(new_table)
        db.session.commit()
        return redirect(f"/projects/{project_id}")

    return render_template('table_create.html', title='Create Table', project_id=project_id, form=table_form)

# Update a table
@project_bp.route('/tables/update/<int:table_id>', methods=['GET', 'POST'])
@login_required
def update_table(table_id):
    table = Table.query.get(table_id)
    table_form = TableForm()

    if table_form.validate_on_submit():
        table.name = request.form['name']
        db.session.commit()
        return redirect(f"/projects/{table.project_id}")

    table_form.name.data = table.name
    return render_template('table_update.html',
                           title='Tables', table_id=table_id, form=table_form)


# Delete a table
@project_bp.route('/tables/del/<int:table_id>', methods=['GET', 'POST'])
@login_required
def delete_table(table_id):
    table = Table.query.get(table_id)
    fields = Field.query.filter(Field.table_id == table.id).all()

    if request.method == 'GET':
        return render_template('table_delete.html', table=table)

    if request.method == 'POST':
        project_id = table.project.id
        fields = Field.query.filter(Field.table_id == table.id).delete()
        db.session.commit()
        db.session.delete(table)
        db.session.commit()
        return redirect(f"/projects/{project_id}")


# Show table details
@project_bp.route('/tables/<int:table_id>', methods=['GET'])
@login_required
def show_table_details(table_id):
    table = Table.query.get(table_id)
    return render_template("table_details.html", title="Table Info", table=table)


#################### ROUTES FOR FIELDS ######################
# Create a Field
@project_bp.route('/tables/<int:table_id>/fields/create', methods=['GET', 'POST'])
@login_required
def create_field(table_id):
    field_form = FieldForm()

    if field_form.validate_on_submit():
        name = request.form['name']
        label = request.form['label']
        placeholder = request.form['placeholder']
        input_type = request.form['input_type']
        required = request.form.get('required') != None
        list_page = request.form.get('list_page') != None
        add_page = request.form.get('add_page') != None
        edit_page = request.form.get('edit_page') != None
        view_page = request.form.get('view_page') != None
        default_val = request.form['default_val']
        kwargs = request.form['kwargs']

        new_field = Field(table_id=table_id, name=name, label=label,
                          placeholder=placeholder, input_type=input_type,
                          required=required, list_page=list_page, add_page=add_page,
                          edit_page=edit_page, view_page=view_page,
                          default_val=default_val, kwargs=kwargs)
        db.session.add(new_field)
        db.session.commit()
        return redirect(f"/projects/tables/{table_id}")

    return render_template('field_create.html', title='Create Field', table_id=table_id, form=field_form)

# Update a Field
@project_bp.route('/tables/fields/update/<int:field_id>', methods=['GET', 'POST'])
@login_required
def update_field(field_id):
    field = Field.query.get(field_id)
    field_form = FieldForm()

    if field_form.validate_on_submit():
        field.name = request.form['name']
        field.label = request.form['label']
        field.placeholder = request.form['placeholder']
        field.input_type = request.form['input_type']
        field.required = request.form.get('required') != None
        field.list_page = request.form.get('list_page') != None
        field.add_page = request.form.get('add_page') != None
        field.edit_page = request.form.get('edit_page') != None
        field.view_page = request.form.get('view_page') != None
        field.default_val = request.form['default_val']
        field.kwargs = request.form['kwargs']

        db.session.commit()
        return redirect(f"/projects/tables/{field.table_id}")

    field_form.name.data = field.name
    field_form.label.data = field.label
    field_form.placeholder.data = field.placeholder
    field_form.input_type.data = field.input_type
    field_form.required.data = field.required
    field_form.list_page.data = field.list_page
    field_form.add_page.data = field.add_page
    field_form.edit_page.data = field.edit_page
    field_form.view_page.data = field.view_page
    field_form.default_val.data = field.default_val
    field_form.kwargs.data = field.kwargs

    return render_template('field_update.html',
                           title='Update Field', field_id=field.id, form=field_form)


# Delete a field
@project_bp.route('/tables/fields/del/<int:field_id>', methods=['GET', 'POST'])
@login_required
def delete_field(field_id):
    field = Field.query.get(field_id)

    if request.method == 'GET':
        return render_template('field_delete.html',
                               title='Delete Field', field=field)

    if request.method == 'POST':
        table_id = field.table_id
        db.session.delete(field)
        db.session.commit()
        return redirect(f"/projects/tables/{table_id}")


# # get data for generation
# @project_bp.route('/<int:project_id>/gendata', methods=['GET'])
# def get_genaration_data(project_id):
#     project = Project.query.get(project_id)
#     project_config = create_config(project)

#     return render_template("project_details.html", title="Project Info", project=project, project_config=project_config)
