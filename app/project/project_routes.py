"""Routes for user pages (Register/Login/Logout/Profile)."""
from flask import Blueprint, render_template, request, flash, redirect, session
from app.models import connect_to_db, db, User, Project
from app.project.project_forms import ProjectForm

# Blueprint Config
project_bp = Blueprint('project_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       url_prefix='/projects')


@project_bp.route('/', methods=['GET'])
def show_projects():
    user_id = session["user_id"]
    projects = Project.query.filter_by(user_id=user_id).all()

    return render_template('projects.html',
                           title='Projects',
                           template='project',
                           body="Projects",
                           projects=projects)


@project_bp.route('/create', methods=['GET', 'POST'])
def create_project():

    if request.method == 'GET':
        return render_template('project_create.html',
                               title='Create a Project',
                               body="Create a Project")

    if request.method == 'POST':
        """Process project creation."""

        # Get form data
        user_id = session["user_id"]
        name = request.form["name"]
        description = request.form["description"]
        db_uri = request.form["db_uri"]

        new_project = Project(user_id=user_id, name=name,
                              description=description, db_uri=db_uri)

        db.session.add(new_project)
        db.session.commit()

        flash(f"Project <b>{name}</b> has been created.")
        return redirect(f"/projects/{new_project.id}")


@project_bp.route('/update/<int:project_id>', methods=['GET', 'POST'])
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
                           title='Projects',
                           body="Update Project",
                           project_id=project_id, form=form)


# show_project_details
@project_bp.route('/<int:project_id>', methods=['GET'])
def show_project_details(project_id):
    project = Project.query.get(project_id)
    return render_template("project_details.html", body="Project Info", project=project)
