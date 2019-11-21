"""Routes for the Code Generator"""
from flask import Blueprint, render_template, request, flash, redirect, session
from app.models import db, Project, Field
from app.gen.coder import write_code
from app.gen.source_dict import source
from app.utils import camel_case
from app.printvar import printvar


# Blueprint Config
gen_bp = Blueprint('gen_bp', __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/gen')


@gen_bp.route('/<int:project_id>')
def generate_code(project_id):
    config = create_config(project_id)
    project_name = config['project_name']

    for (index, table) in enumerate(config["tables"]):
        """Call generator functions for every table(module)"""
        model_name = config['tables_camelcase'][index]
        tconfig = config[table]
        templates = config['templates'][table]
        gen_mod_inifile(project_name, table)
        gen_mod_css(project_name, table)
        gen_mod_templates(project_name, table, tconfig, templates)
        gen_routes(project_name, model_name, table, tconfig['tschema'])
        gen_wtforms(project_name, model_name, table, tconfig['tschema'])

    gen_source_files(project_name, config["tables"])
    gen_models(config)
    gen_user_links(project_name, config["tables"])

    return render_template('generator.html')


def create_config(project_id):
    """Creates dictionary of configurations for generating codes"""
    project = Project.query.get(project_id)
    schema = create_schema(project)
    tables = [table for table in schema]

    config = {}
    config["project_name"] = project.name
    config["conn"] = project.db_uri
    config["tables"] = tables
    config["tables_camelcase"] = [camel_case(table) for table in tables]
    config["templates"] = get_templates(project)

    # tschema = table schema
    for table in tables:
        tschema = schema[table]
        config[table] = {
            "tschema": tschema,
            "create_fields": [field for field in tschema if tschema[field]['add']],
            "update_fields": [field for field in tschema if tschema[field]['edit']],
            "details_fields": [field for field in tschema if tschema[field]['view']],
            "list_fields": [field for field in tschema if tschema[field]['list']],
            "delete_fields": [field for field in tschema if tschema[field]['view']],
        }
    return config


# ----------------Config functions--------------#
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
                "default_val": field.default_val,
                "kwargs": field.kwargs
            }

    return schema


# ----------------HTML Templates--------------#
def get_templates(prj_model):
    """Get the html templates of each table for a given project.
    prj_model is equal to Project.query.get(id)
    """
    templates = {}
    for table in prj_model.tables:
        templates[table.name] = {}
        if table.page_templates:
            tpl = table.page_templates
            templates[table.name] = {
                # templates.get(f"{file}_kwargs")
                'list': tpl.list_page if tpl.list_page else 'default',
                'list_kwargs': tpl.list_kwargs,
                'create': tpl.add_page if tpl.add_page else 'default',
                'create_kwargs': tpl.add_kwargs,
                'update': tpl.edit_page if tpl.edit_page else 'default',
                'update_kwargs': tpl.edit_kwargs,
                'details': tpl.view_page if tpl.view_page else 'default',
                'details_kwargs': tpl.view_kwargs,
                'delete': tpl.delete_page if tpl.delete_page else 'default',
                'delete_kwargs': tpl.delete_kwargs
            }
        else:
            templates[table.name] = {
                'list': 'default',
                'create': 'default',
                'update': 'default',
                'details': 'default',
                'delete': 'default'
            }

    return templates


# ----------------models.py Generator--------------#
def gen_models(config):
    src_path = "source/app"
    src_file = "models.txt"
    kwargs = config
    output_obj = {"output_path": f"{config['project_name']}/app",
                  "output_file": "models.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------routes Generator--------------#
def gen_routes(project_name, model_name, table, table_schema):
    src_path = "source/app/module"
    src_file = "routes.txt"
    kwargs = {}
    kwargs['project_name'] = project_name
    kwargs['model_name'] = model_name
    kwargs['table'] = table
    kwargs['table_schema'] = table_schema
    output_obj = {"output_path": f"{project_name}/app/mod_{table}",
                  "output_file": f"{table}_routes.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


def gen_wtforms(project_name, model_name, table, table_schema):
    src_path = "source/app/module"
    src_file = "forms.txt"
    kwargs = {}
    kwargs['model_name'] = model_name
    kwargs['table'] = table
    kwargs['table_schema'] = table_schema
    output_obj = {"output_path": f"{project_name}/app/mod_{table}",
                  "output_file": f"{table}_form.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------HTML Templates Generator--------------#
def gen_mod_templates(project_name, table, tconfig, templates):
    src_path = "source/app/module/templates"
    files = ['create', 'update', 'details', 'list', 'delete']
    kwargs = {}
    kwargs["table"] = table
    kwargs["tschema"] = tconfig["tschema"]

    for file in files:
        src_file = f"{file}_{templates[file]}.html"
        output_file = f"{table}_{file}.html"
        fields = f"{file}_fields"
        output_obj = {"output_path": f"{project_name}/app/mod_{table}/templates",
                      "output_file": output_file}
        kwargs[fields] = tconfig[fields]
        kwargs[f"{file}_kwargs"] = templates.get(f"{file}_kwargs")
        write_code(src_path, src_file, kwargs, output_obj)

    return None


# ----------------__init__.py Generator for every module--------------#
def gen_mod_inifile(project_name, table):
    src_path = "source/app/module"
    src_file = "__init__.txt"
    kwargs = {}
    output_obj = {"output_path": f"{project_name}/app/mod_{table}",
                  "output_file": "__init__.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------style.css Generator for every module--------------#
def gen_mod_css(project_name, table):
    src_path = "source/app/module/static/css"
    src_file = "style.css"
    kwargs = {}
    output_obj = {"output_path": f"{project_name}/app/mod_{table}",
                  "output_file": "style.css"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------Generate other files from source templates--------------#
def gen_source_files(project_name, tables):
    """Generate other files from source templates"""
    for k, v in source.items():
        filenames = v.split()
        src_path = k.split('__')[0]
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


def gen_user_links(project_name, tables):
    src_path = "source/app/templates"
    src_file = "user_links.html"
    kwargs = {}
    kwargs['tables'] = tables
    output_obj = {"output_path": f"{project_name}/app/templates",
                  "output_file": "user_links.html"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None
    pass
