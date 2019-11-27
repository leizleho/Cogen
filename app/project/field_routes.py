from flask import render_template, request, flash, redirect, session
from app.models import db, Field
from app.project import project_bp
from flask_login import current_user, login_required
from app.project.forms import FieldForm

#################### ROUTES FOR FIELDS ######################
# Create a Field
@project_bp.route('/tables/<int:table_id>/fields/create', methods=['GET', 'POST'])
@login_required
def create_field(table_id):
    form = FieldForm()

    if form.validate_on_submit():
        name = form.name.data
        label = form.label.data
        placeholder = form.placeholder.data
        input_type = form.input_type.data
        required = form.required.data
        list_page = form.list_page.data
        add_page = form.add_page.data
        edit_page = form.edit_page.data
        view_page = form.view_page.data
        default_val = form.default_val.data
        foreign_key = form.foreign_key.data
        kwargs = form.kwargs.data

        new_field = Field(table_id=table_id, name=name, label=label,
                          placeholder=placeholder, input_type=input_type,
                          required=required, list_page=list_page, add_page=add_page,
                          edit_page=edit_page, view_page=view_page,
                          default_val=default_val, foreign_key=foreign_key,
                          kwargs=kwargs)
        db.session.add(new_field)
        db.session.commit()
        return redirect(f"/projects/tables/{table_id}")

    return render_template('field_create.html', title='Create Field', table_id=table_id, form=form)

# Update a Field
@project_bp.route('/tables/fields/update/<int:field_id>', methods=['GET', 'POST'])
@login_required
def update_field(field_id):
    field = Field.query.get(field_id)
    form = FieldForm()

    if form.validate_on_submit():
        field.name = form.name.data
        field.label = form.label.data
        field.placeholder = form.placeholder.data
        field.input_type = form.input_type.data
        field.required = form.required.data
        field.list_page = form.list_page.data
        field.add_page = form.add_page.data
        field.edit_page = form.edit_page.data
        field.view_page = form.view_page.data
        field.default_val = form.default_val.data
        field.foreign_key = form.foreign_key.data
        field.kwargs = form.kwargs.data

        db.session.commit()
        return redirect(f"/projects/tables/{field.table_id}")

    form.name.data = field.name
    form.label.data = field.label
    form.placeholder.data = field.placeholder
    form.input_type.data = field.input_type
    form.required.data = field.required
    form.list_page.data = field.list_page
    form.add_page.data = field.add_page
    form.edit_page.data = field.edit_page
    form.view_page.data = field.view_page
    form.default_val.data = field.default_val
    form.foreign_key.data = field.foreign_key
    form.kwargs.data = field.kwargs

    return render_template('field_update.html',
                           title='Update Field', field_id=field.id, form=form)


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
