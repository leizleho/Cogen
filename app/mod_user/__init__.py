from flask import Blueprint

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/users')

from app.mod_user import user_routes
