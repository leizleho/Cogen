from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# temporary secret key
app.secret_key = "ABC"

# initialize bootstrap
bootstrap = Bootstrap(app)

# Flask-Login configs
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user_bp.login"


# import blueprints after initializing login_manager
from app.user.user_routes import user_bp
from app.main.main_routes import main_bp
from app.project.project_routes import project_bp
from app.gen.gen_routes import gen_bp

# Register blueprints with the app
app.register_blueprint(main_bp)
app.register_blueprint(user_bp)
app.register_blueprint(project_bp)
app.register_blueprint(gen_bp)
