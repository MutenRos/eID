"""Rutas de perfil de usuario"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.social_link import SocialLink

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/me')
@login_required
def my_profile():
    """Mi perfil"""
    return render_template('profile/view.html', user=current_user)

@bp.route('/<username>')
def view_profile(username):
    """Ver perfil de otro usuario"""
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile/view.html', user=user)

@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Editar perfil"""
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.bio = request.form.get('bio')
        current_user.website = request.form.get('website')
        db.session.commit()
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
        
        link = SocialLink(
            user_id=current_user.id,
            platform=platform,
            username=username,
            url=url
        )
        db.session.add(link)
        db.session.commit()
        flash(f'Red social {platform} agregada', 'success')
        return redirect(url_for('profile.social_links'))
    
    links = current_user.social_links.order_by(SocialLink.order).all()
    return render_template('profile/social_links.html', links=links)

@bp.route('/social-links/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_social_link(link_id):
    """Eliminar enlace a red social"""
    link = SocialLink.query.get_or_404(link_id)
    if link.user_id != current_user.id:
        flash('No autorizado', 'error')
        return redirect(url_for('profile.social_links'))
    
    db.session.delete(link)
    db.session.commit()
    flash('Red social eliminada', 'success')
    return redirect(url_for('profile.social_links'))
