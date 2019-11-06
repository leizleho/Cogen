"""Routes for user pages (Register/Login/Logout/Profile)."""
from flask import Blueprint, render_template, request, flash, redirect, session
from flask import current_app as app
from app.models import connect_to_db, db, User


# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/users')


@user_bp.route('/register')
def register_form():
    """User Registration page"""

    return render_template('register.html',
                           title='User Registration',
                           template='register',
                           body="User Registration")


@user_bp.route('/register', methods=['POST'])
def register():
    """Process registration."""
    # Get form variables
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(fname=fname, lname=lname, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {fname} {lname} is added.")
    return redirect(f"/users/{new_user.id}")


@user_bp.route('/login')
def login_form():
    """User Login page"""

    return render_template('login.html',
                           title='User Login',
                           template='login',
                           body="User Login")


@user_bp.route('/login', methods=['POST'])
def login():
    """Process login."""
    # Get form variables
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/users/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/users/login")

    session["user_id"] = user.id

    flash("Logged in")
    return redirect(f"/users/{user.id}")


@user_bp.route('/logout')
def logout():
    """Log out."""

    session.clear()
    flash("Logged Out.")
    return redirect("/")


@user_bp.route("/<int:user_id>")
def user_info(user_id):
    """Show info about user."""
    user = User.query.options(db.joinedload(
        'projects')).get(user_id)
    return render_template("user.html", body="User Info", user=user)
