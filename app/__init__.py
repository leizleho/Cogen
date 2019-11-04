from flask import Flask
from app.auth import auth_routes
app = Flask(__name__)

app.register_blueprint(auth_routes.auth_bp)
