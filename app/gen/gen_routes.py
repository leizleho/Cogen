"""Routes for the Code Generator"""
from flask import Blueprint, render_template, request, flash, redirect, session
from app.models import db, Project, Field
from app.gen.coder import write_code
from app.gen.source_dict import source
from app.utils import camel_case
# from app.printvar import printvar

# Blueprint Config
gen_bp = Blueprint('gen_bp', __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/gen')


@gen_bp.route('/<int:project_id>')
def generate_code(project_id):
    config = create_config(project_id)
    for table in config["tables"]:
        gen_add_fields(config['project_name'], table, config[table])
        gen_edit_fields(config['project_name'], table, config[table])

    gen_source_files(config['project_name'], config["tables"])

    return "Todo"


def create_config(project_id):
    project = Project.query.get(project_id)
    schema = create_schema(project)
    tables = [table for table in schema]
    tables_camelcase = [camel_case(table) for table in schema]

    config = {}
    config["project_name"] = project.name
    config["conn"] = project.db_uri
    config["tables"] = tables
    config["tables_camelcase"] = tables_camelcase

    add_fields = edit_fields = view_fields = []

    # tschema = table schema
    for table in tables:
        tschema = schema[table]
        config[table] = {
            "tschema": tschema,
            "add_fields": [field for field in tschema if tschema[field]['add']],
            "edit_fields": [field for field in tschema if tschema[field]['edit']],
            "view_fields": [field for field in tschema if tschema[field]['view']]
        }
    return config


# ----------------models.py Generator--------------#

def gen_models(config):
    src_path = "source/app"
    src_file = "models.txt"
    kwargs = config
    output_obj = {"output_path": f"{config['project_name']}/app",
                  "output_file": "models.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------HTML Templates Generator--------------#

def gen_add_fields(project_name, table, tconfig):
    """Generate template for create.html page"""
    src_path = "source/app/module/templates"
    src_file = "create.html"
    kwargs = {}
    kwargs["tschema"] = tconfig["tschema"]
    kwargs["add_fields"] = tconfig["add_fields"]
    output_obj = {"output_path": f"{project_name}/app/mod_{table}/templates",
                  "output_file": f"{table}_create.html"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


def gen_edit_fields(project_name, table, tconfig):
    src_path = "source/app/module/templates"
    src_file = "update.html"
    kwargs = {}
    kwargs["tschema"] = tconfig["tschema"]
    kwargs["edit_fields"] = tconfig["edit_fields"]
    output_obj = {"output_path": f"{project_name}/app/mod_{table}/templates",
                  "output_file": f"{table}_update.html"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None

# ----------------End of HTML Templates Generator--------------#


# ----------------Helper functions--------------#

def gen_source_files(project_name, tables):
    """Generate other files from source templates"""
    for k, v in source.items():
        filenames = v.split()
        src_path = k.split('_')[0]
        src_file = filenames[0]
        output_file = filenames[1]
        output_path = src_path.replace("source", project_name)
        output_obj = {
            "output_path": output_path,
            "output_file": output_file
        }
        kwargs = {
            "tables": tables
        }

        write_code(src_path, src_file, kwargs, output_obj)

    return None


# ----------------Helper functions--------------#

def create_schema(prj_model):
    """Create schema of each table for a given project.
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
