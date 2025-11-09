"""Rutas de perfil de usuario"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.social_link import SocialLink

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/me')
@login_required
def my_profile():
    """Mi perfil"""
    social_links = SocialLink.get_by_user(current_user.id)
    return render_template('profile/view.html', user=current_user, social_links=social_links)

@bp.route('/<username>')
def view_profile(username):
    """Ver perfil de otro usuario"""
    user = User.find_by_username(username)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('main.index'))
    
    social_links = SocialLink.get_visible_by_user(user.id)
    return render_template('profile/view.html', user=user, social_links=social_links)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Editar perfil"""
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        bio = request.form.get('bio')
        website = request.form.get('website')
        
        current_user.update(full_name, bio, website)
        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('profile.my_profile'))
    
    return render_template('profile/edit.html')

@bp.route('/social-links', methods=['GET', 'POST'])
@login_required
def social_links():
    """Gestionar enlaces a redes sociales"""
    if request.method == 'POST':
        platform = request.form.get('platform')
        username = request.form.get('username')
        url = request.form.get('url')
        
        SocialLink.create(current_user.id, platform, username, url)
        flash(f'Red social {platform} agregada', 'success')
        return redirect(url_for('profile.social_links'))
    
    links = SocialLink.get_by_user(current_user.id)
    return render_template('profile/social_links.html', links=links)

@bp.route('/social-links/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_social_link(link_id):
    """Eliminar enlace a red social"""
    SocialLink.delete(link_id, current_user.id)
    flash('Red social eliminada', 'success')
    return redirect(url_for('profile.social_links'))
