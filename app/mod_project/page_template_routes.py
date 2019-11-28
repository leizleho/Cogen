from flask import render_template, request, flash, redirect, session
from app.db import db
from app.models.pagetemplate import PageTemplate
from app.mod_project import project_bp
from flask_login import current_user, login_required
from app.mod_project.forms import PageTemplateForm

# Add templates
@project_bp.route('/tables/<int:table_id>/templates/add', methods=['GET', 'POST'])
@login_required
def add_template(table_id):
    form = PageTemplateForm()
    if form.validate_on_submit():
        list_page = form.list_page.data
        list_kwargs = form.list_kwargs.data
        add_page = form.add_page.data
        add_kwargs = form.add_kwargs.data
        edit_page = form.edit_page.data
        edit_kwargs = form.edit_kwargs.data
        view_page = form.view_page.data
        view_kwargs = form.view_kwargs.data
        delete_page = form.delete_page.data
        delete_kwargs = form.delete_kwargs.data

        new_templates = PageTemplate(table_id=table_id, list_page=list_page,
                                     list_kwargs=list_kwargs,
                                     add_page=add_page,
                                     add_kwargs=add_kwargs,
                                     edit_page=edit_page,
                                     edit_kwargs=edit_kwargs,
                                     view_page=view_page,
                                     view_kwargs=view_kwargs,
                                     delete_page=delete_page,
                                     delete_kwargs=delete_kwargs)
        db.session.add(new_templates)
        db.session.commit()
        return redirect(f"/projects/{table_id}")

    return render_template('page_template_create.html', title='Add Templates', table_id=table_id, form=form)


# Update a table
@project_bp.route('/tables/<int:table_id>/templates/update/<int:template_id>', methods=['GET', 'POST'])
@login_required
def update_template(table_id, template_id):
    templates = PageTemplate.query.get(template_id)
    form = PageTemplateForm()

    if form.validate_on_submit():
        templates.list_page = form.list_page.data
        templates.list_kwargs = form.list_kwargs.data
        templates.add_page = form.add_page.data
        templates.add_kwargs = form.add_kwargs.data
        templates.edit_page = form.edit_page.data
        templates.edit_kwargs = form.edit_kwargs.data
        templates.view_page = form.view_page.data
        templates.view_kwargs = form.view_kwargs.data
        templates.delete_page = form.delete_page.data
        templates.delete_kwargs = form.delete_kwargs.data
        db.session.commit()
        return redirect(f"/tables/{table_id}/templates")

    form.list_page.data = templates.list_page
    form.list_kwargs.data = templates.list_kwargs
    form.add_page.data = templates.add_page
    form.add_kwargs.data = templates.add_kwargs
    form.edit_page.data = templates.edit_page
    form.edit_kwargs.data = templates.edit_kwargs
    form.view_page.data = templates.view_page
    form.view_kwargs.data = templates.view_kwargs
    form.delete_page.data = templates.delete_page
    form.delete_kwargs.data = templates.delete_kwargs
    return render_template('page_template_update.html',
                           title='Tables', table_id=table_id, template_id=template_id, form=form)
