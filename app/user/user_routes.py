"""Routes for user pages (Register/Login/Logout/Profile)."""
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask import current_app as app
from flask_login import login_user, current_user, logout_user, login_required
from app import login_manager
from app.models import connect_to_db, db, User
from app.user.user_forms import LoginForm, RegistrationForm


# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__,
                    template_folder='templates',
                    static_folder='static',
                    url_prefix='/users')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')

    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(fname=form.fname.data,
                        lname=form.lname.data,
                        username=form.username.data,
                        email=form.email.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()
        flash('User registration is complete!')
        return redirect(url_for('user_bp.login'))

    return render_template('register.html', form=form, title='User Registration')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            # Log in the user
            login_user(user)
            flash('Logged in successfully.')
            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # Check if that next exists, otherwise go to home page
            if next == None or not next[0] == '/':
                next = url_for('user_bp.user_info', user_id=user.id)
            return redirect(next)
        else:
            flash('Invalid email or password')
            return redirect(url_for('user_bp.login'))

    return render_template('login.html', title='Login', form=form)


@user_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main_bp.home'))


@user_bp.route("/<int:user_id>")
@login_required
def user_info(user_id):
    """Show info about user."""
    user = User.query.options(db.joinedload(
        'projects')).get(user_id)
    return render_template("user.html", body="User Info", user=user)
