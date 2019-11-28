from flask import Blueprint

# Blueprint Configuration
main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates',
                    static_folder='static')

from app.mod_main import main_routes
