"""Routes for the Code Generator"""
from flask import Blueprint, render_template, request, flash, redirect, session
from app.models import db, Project, Field
from app.gen.coder import write_code

# Blueprint Config
gen_bp = Blueprint('gen_bp', __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/gen')


@gen_bp.route('/<int:project_id>')
def generate_codes(project_id):
    # name, conn, schema
    project = Project.query.get(project_id)
    name = project.name
    conn = project.db_uri
    schema = create_schema(project)

    # get list of tables
    tables = [table for table in schema]
    add_fields = edit_fields = view_fields = []

    # tschema = table schema
    for table in tables:
        tschema = schema[table]
        add_fields = [field for field in tschema if tschema[field]['add']]
        edit_fields = [field for field in tschema if tschema[field]['edit']]
        view_fields = [field for field in tschema if tschema[field]['view']]

    return "Todo"


# ----------------Helper functions--------------#

def create_schema(prj_model):
    """Create schema for a given project.
    prj_model is equal to Project.query.get(id)
    """
    schema = {}
    for table in prj_model.tables:
        schema[table.name] = {}
        for field in table.fields:
            schema[table.name][field.name] = {
                "label": field.label,
                "placeholder": field.placeholder,
                "input_type": field.input_type,
                "required": field.required,
                "list": field.list_page,
                "add": field.add_page,
                "edit": field.edit_page,
                "view": field.view_page,
                "default_val": field.default_val
            }
    return schema
