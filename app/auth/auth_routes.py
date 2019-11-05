"""Routes for Auth pages (Register/Login/Logout/Profile)."""
from flask import Blueprint, render_template, request, flash, redirect, session
from flask import current_app as app
from app.models import connect_to_db, db, User


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/auth')


@auth_bp.route('/profile')
def me():
    """User profile page"""

    user = User.query.filter_by(id=1).one()

    return render_template('profile.html',
                           title='Profile',
                           template='profile',
                           body="Profile Page", user=user)


@auth_bp.route('/register')
def register_form():
    """User Registration page"""

    return render_template('register.html',
                           title='User Registration',
                           template='register',
                           body="User Registration")


@auth_bp.route('/register', methods=['POST'])
def register():
    """Process registration."""
    # Get form variables
    fname = int(request.form["fname"])
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {fname} {lname} is added.")
    return redirect(f"/users/{new_user.user_id}")
