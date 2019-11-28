from flask import render_template, request, flash, redirect, session
from app.db import db
from app.models.table import Table
from app.models.field import Field
from app.mod_project import project_bp
from flask_login import current_user, login_required
from app.mod_project.forms import TableForm

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
