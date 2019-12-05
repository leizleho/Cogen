from app.mod_gen.coder import write_code
from app.mod_gen.source_dict import source


# ----------------models.py Generator--------------#
def gen_models(config):
    src_path = "source/app"
    src_file = "models.txt"
    kwargs = config
    output_obj = {"output_path": f"{config['project_name']}/app",
                  "output_file": "models.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------server.py Generator--------------#
def gen_server(project_name, port):
    src_path = "source"
    src_file = "server.txt"
    kwargs = {}
    kwargs['port'] = port
    output_obj = {"output_path": f"{project_name}",
                  "output_file": "server.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------routes Generator--------------#
def gen_routes(project_name, model_name, table, tconfig):
    src_path = "source/app/module"
    src_file = "routes.txt"
    kwargs = {}
    kwargs['project_name'] = project_name
    kwargs['model_name'] = model_name
    kwargs['table'] = table
    kwargs['table_schema'] = tconfig['tschema']
    kwargs['image_fields'] = tconfig['image_fields']
    output_obj = {"output_path": f"{project_name}/app/mod_{table}",
                  "output_file": f"{table}_routes.py"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None


# ----------------WTForms Generator--------------#
def gen_wtforms(project_name, model_name, table, tconfig):
    src_path = "source/app/module"
    src_file = "forms.txt"
    kwargs = {}
    kwargs['model_name'] = model_name
    kwargs['table'] = table
    kwargs['table_schema'] = tconfig['tschema']
    kwargs['input_types'] = tconfig['input_types']
    kwargs['wtf_formfields'] = tconfig['wtf_formfields']
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
    kwargs['image_fields'] = tconfig['image_fields']

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


# ----------------Nav Links Generator--------------#
def gen_user_links(project_name, tables):
    src_path = "source/app/templates"
    src_file = "user_links.html"
    kwargs = {}
    kwargs['tables'] = tables
    output_obj = {"output_path": f"{project_name}/app/templates",
                  "output_file": "user_links.html"}
    write_code(src_path, src_file, kwargs, output_obj)
    return None
