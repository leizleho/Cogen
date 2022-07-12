import os
from app.mod_gen.coder import write_code
from app.mod_gen.source_dict import source


# ----------------uwsgi.ini Generator--------------#
def gen_app_uwsgi(project_name, port):
    src_path = "source/uwsgi"
    src_file = "app.ini"
    app_dir_parent = os.path.abspath(os.path.join(__file__, "../../.."))
    app_dir = os.path.join(app_dir_parent, "builds", project_name)
    # app_dir = os.path.join(app_dir_parent, "builds", project_name, "app")
    out_dir = os.path.join(app_dir_parent, "uwsgi/vassals")
    kwargs = {}
    kwargs['port'] = port
    kwargs['dir'] = app_dir
    output_file = f"{project_name}_app.ini"
    output_obj = {"output_path": f"{project_name}/app",
                  "output_file": output_file}
    write_code(src_path, src_file, kwargs, output_obj, out_dir)
    return None


# ----------------uwsgi.ini Generator--------------#
def gen_db_uwsgi(project_name, port):
    src_path = "source/uwsgi"
    src_file = "db.ini"
    app_dir_parent = os.path.abspath(os.path.join(__file__, "../../.."))
    app_dir = os.path.join(app_dir_parent, "builds", project_name, "app")
    out_dir = os.path.join(app_dir_parent, "uwsgi/vassals")
    kwargs = {}
    kwargs['port'] = port
    kwargs['dir'] = app_dir
    output_file = f"{project_name}_db.ini"
    output_obj = {"output_path": f"{project_name}/app",
                  "output_file": output_file}
    write_code(src_path, src_file, kwargs, output_obj, out_dir)
    return None
