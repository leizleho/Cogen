from flask import Flask
from flask_login import LoginManager
# from flask_restful import Api

# from app.api.resources.table import Table, Tables
# from app.api.resources.project import Project, Projects

app = Flask(__name__)

# temporary secret key
app.secret_key = "ABC"
# api = Api(app)

# Flask-Login configs
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_bp.login"


# import blueprints after initializing login_manager
from app.mod_user import user_bp
from app.mod_main import main_bp
from app.mod_project import project_bp
from app.mod_gen import gen_bp
from app.api import api_bp

# Register blueprints with the app
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(project_bp)
app.register_blueprint(gen_bp)
app.register_blueprint(api_bp)

# Endpoints for the API module
# api.add_resource(Table, "/api/table/<string:name>")
# api.add_resource(Tables, "/api/tables")
# api.add_resource(Project, "/api/project/<string:name>")
# api.add_resource(Projects, "/api/projects")
