from flask import render_template, request, flash, redirect, session
from app.db import db
from app.models.relationship import Relationship
from app.models.table import Table
from app.mod_project import project_bp
from flask_login import current_user, login_required
from app.mod_project.forms import RelationshipForm

# Create Relationships
@project_bp.route('/<int:project_id>/tables/<int:table_id>/relationships/create', methods=['GET', 'POST'])
@login_required
def create_relationship(project_id, table_id):
    form = RelationshipForm()
    parent_tbl = Table.query.get(table_id)

    tables = Table.query.filter(
        Table.id != table_id, Table.project_id == project_id)
    choices = []
    for table in tables:
        choices.append((table.name, table.name))

    form.child_table.choices = choices

    if form.validate_on_submit():
        rel_type = form.rel_type.data
        rel_name = form.rel_name.data
        parent_table = parent_tbl.name
        child_table = form.child_table.data

        new_rel = Relationship(table_id=table_id, rel_type=rel_type,
                               rel_name=rel_name, parent_table=parent_table,
                               child_table=child_table, )
        db.session.add(new_rel)
        db.session.commit()
        return redirect(f"/projects/{table_id}")

    return render_template('relationship_create.html',
                           project_id=project_id,
                           table_id=table_id,
                           table_name=parent_tbl.name,
                           form=form)
