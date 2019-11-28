"""Routes for main pages."""
from flask import render_template
from app.mod_main import main_bp


@main_bp.route('/')
def home():
    """Homepage route."""
    return render_template('index.html',
                           title='Cogen - Code Generator App',
                           template='home',
                           body='Home')
