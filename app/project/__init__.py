from flask import Blueprint

# Blueprint Config
project_bp = Blueprint('project_bp', __name__,
                       template_folder='templates',
                       static_folder='static',
                       url_prefix='/projects')

from app.project import project_routes, table_routes, field_routes, page_template_routes, relationship_routes
