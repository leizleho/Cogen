from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager

from app.mod_api.blacklist import BLACKLIST
from app.mod_api.resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from app.mod_api.resources.project import Project, Projects
# from app.api.resources.table import Table, Tables

app = Flask(__name__)

# temporary secret key
app.secret_key = "ABC"
api = Api(app)

# Flask-Login configs
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_bp.login"


# import blueprints after initializing login_manager
from app.mod_user import user_bp
from app.mod_main import main_bp
from app.mod_project import project_bp
from app.mod_gen import gen_bp
from app.mod_api import api_bp

# Register blueprints with the app
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(project_bp)
app.register_blueprint(gen_bp)
app.register_blueprint(api_bp)


jwt = JWTManager(app)

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


# Endpoints for the API module
api.add_resource(UserRegister, "/api/register")
api.add_resource(User, "/api/user/<int:id>")
api.add_resource(UserLogin, "/api/login")
api.add_resource(TokenRefresh, "/api/refresh")
api.add_resource(UserLogout, "/api/logout")
api.add_resource(Projects, "/api/projects")
api.add_resource(Project, "/api/project",
                          "/api/project/<int:id>")
# api.add_resource(Table, "/api/table/<string:name>")
# api.add_resource(Tables, "/api/tables")
