"""Routes for the Code Generator"""
from flask import render_template
from app.mod_gen import gen_bp
from app.models.project import Project
from app.mod_gen.gen_config import create_config
import app.mod_gen.gen_files as gen
from app.mod_gen.gen_uwsgi import gen_app_uwsgi, gen_db_uwsgi
import subprocess
import os


@gen_bp.route('/<int:project_id>')
def show_generationpage(project_id):
    config = create_config(project_id, all=False)
    return render_template('generator.html', project_id=project_id, config=config)


@gen_bp.route('/generatecodes/<int:project_id>', methods=['GET'])
def gen_codes(project_id):
    """Function for generating all files"""

    config = create_config(project_id)
    project_name = config['project_name']

    for (index, table) in enumerate(config["tables"]):
        """Call generator functions for every table(module)"""
        model_name = config['tables_camelcase'][index]
        tconfig = config[table]
        templates = config['templates'][table]
        gen.gen_mod_inifile(project_name, table)
        gen.gen_mod_css(project_name, table)
        gen.gen_mod_templates(project_name, table, tconfig, templates)
        gen.gen_routes(project_name, model_name, table, tconfig)
        gen.gen_wtforms(project_name, model_name, table, tconfig)

    gen.gen_source_files(project_name, config["tables"])
    gen.gen_models(config)
    gen.gen_server(project_name, config["app_port"])
    gen.gen_user_links(project_name, config["tables"])
    gen.gen_layout(project_name, config["brand"])
    return "Code generation is complete!"


@gen_bp.route('/initdb/<int:project_id>')
def gen_uwsgi_db(project_id):
    config = create_config(project_id, all=False)
    project_name = config['project_name']

    app_dir_parent = os.path.abspath(os.path.join(__file__, "../../.."))
    app_dir = os.path.join(app_dir_parent, "builds", project_name, "app")
    subprocess.run(['python3', 'models.py'], cwd=app_dir)
    return "DB Setup is complete!"


@gen_bp.route('/runapp/<int:project_id>')
def gen_uwsgi_app(project_id):
    config = create_config(project_id, all=False)
    project_name = config['project_name']

    gen_app_uwsgi(project_name, config["app_port"])
    link = f"http://localhost:{config['app_port']}"

    return f'Your app is running on <a target="_blank" href="{link}">{link}</a>'
