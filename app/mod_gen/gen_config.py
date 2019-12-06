from app.models.project import Project
from app.utils import camel_case
from app.mod_gen.source_dict import wtf

PORT = 5555


def create_config(project_id, all=True):
    """Creates dictionary of configurations for generating codes"""
    project = Project.query.get(project_id)
    schema = create_schema(project)
    tables = [table for table in schema]
    project_config = {}

    if not all:
        project_config["project_id"] = project.id
        project_config["project_name"] = project.name
        project_config["conn"] = project.db_uri
        project_config["app_port"] = PORT + int(project_id)
        project_config["dbinit_port"] = PORT - int(project_id)
        return project_config

    config = {}
    config["project_id"] = project.id
    config["project_name"] = project.name
    config["brand"] = project.brand
    config["conn"] = project.db_uri
    config["app_port"] = PORT + int(project_id)
    config["tables"] = tables
    config["tables_camelcase"] = [camel_case(table) for table in tables]
    config["templates"] = get_templates(project)

    # tschema = table schema
    for table in tables:
        tschema = schema[table]
        input_types = set([tschema[field]['input_type'] for field in tschema])
        config[table] = {
            "tschema": tschema,
            "input_types": input_types,
            "wtf_formfields": ', '.join(set([wtf[input_type] for input_type in input_types])),
            "image_fields": [field for field in tschema if tschema[field]['input_type'] == 'image'],
            "create_fields": [field for field in tschema if tschema[field]['add']],
            "update_fields": [field for field in tschema if tschema[field]['edit']],
            "details_fields": [field for field in tschema if tschema[field]['view']],
            "list_fields": [field for field in tschema if tschema[field]['list']],
            "delete_fields": [field for field in tschema if tschema[field]['view']]
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
