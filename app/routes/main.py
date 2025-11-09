"""Rutas principales"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Página principal"""
    if current_user.is_authenticated:
        return redirect(url_for('profile.my_profile'))
    return render_template('index.html')

@bp.route('/about')
def about():
    """Acerca de eID"""
    return render_template('about.html')
