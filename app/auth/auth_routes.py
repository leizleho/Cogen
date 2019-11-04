"""Routes for Auth pages (Register/Login/Logout/Profile)."""
from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/auth')


@auth_bp.route('/profile')
def me():
    """User profile page"""
    return render_template('profile.html',
                           title='Profile',
                           template='profile',
                           body="Profile Page")
