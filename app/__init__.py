from flask import Flask
from app.user import user_routes
from app.main import main_routes
from app.project import project_routes
from app.gen import gen_routes

app = Flask(__name__)

# temporary secret key
app.secret_key = "ABC"

app.register_blueprint(main_routes.main_bp)
app.register_blueprint(user_routes.user_bp)
app.register_blueprint(project_routes.project_bp)
app.register_blueprint(gen_routes.gen_bp)
