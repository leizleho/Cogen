"""Routes for projects"""
from flask import render_template, request, flash, redirect, session
from app.db import db
from app.models.user import User
from app.models.project import Project
from app.models.table import Table
from app.models.field import Field
from app.mod_project import project_bp
from flask_login import current_user, login_required
from app.mod_project.forms import ProjectForm

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
    form = ProjectForm()
    if form.validate_on_submit():
        # Get form data
        user_id = current_user.id
        name = form.name.data
        description = form.description.data
        brand = form.brand.data
        logo = form.logo.data
        db_uri = form.db_uri.data

        new_project = Project(user_id=user_id, name=name,
                              description=description, brand=brand,
                              logo=logo, db_uri=db_uri)

        db.session.add(new_project)
        db.session.commit()
        flash(f"Project {name} has been created.")
        return redirect(f"/projects/{new_project.id}")

    return render_template('project_create.html', title="Create Project", form=form)


@project_bp.route('/update/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get(project_id)
    form = ProjectForm()

    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.brand = form.brand.data
        project.logo = form.logo.data
        project.db_uri = form.db_uri.data
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
