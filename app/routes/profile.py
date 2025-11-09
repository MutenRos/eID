"""Rutas de perfil de usuario"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.social_link import SocialLink
from app.models.contact import Contact
from app.social_extractor import extract_social_info
import json

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/me')
@login_required
def my_profile():
    """Mi perfil"""
    social_links = SocialLink.get_by_user(current_user.id)
    
    # Crear diccionario de links por plataforma para pre-llenar formularios
    links_dict = {}
    for link in social_links:
        # DEBUG: Ver qué tipo de dato es profile_data
        print(f"\n=== DEBUG: {link['platform']} ===")
        print(f"Type of profile_data: {type(link.get('profile_data'))}")
        print(f"Value: {link.get('profile_data')}")
        
        # Parsear profile_data si existe y es string
        if link.get('profile_data'):
            try:
                if isinstance(link['profile_data'], str):
                    print("Es string, parseando JSON...")
                    link['profile_data_parsed'] = json.loads(link['profile_data'])
                    print(f"Parseado exitosamente: {link['profile_data_parsed']}")
                elif isinstance(link['profile_data'], dict):
                    print("Ya es dict, usando directamente")
                    link['profile_data_parsed'] = link['profile_data']
                else:
                    print(f"Tipo desconocido: {type(link['profile_data'])}")
                    link['profile_data_parsed'] = None
            except Exception as e:
                print(f"❌ Error parseando profile_data: {e}")
                link['profile_data_parsed'] = None
        else:
            link['profile_data_parsed'] = None
            
        links_dict[link['platform']] = link
    
    return render_template('profile/view.html', user=current_user, social_links=social_links, links_dict=links_dict, is_own_profile=True)

@bp.route('/contact/<int:user_id>')
@login_required
def view_contact(user_id):
    """Ver perfil de un contacto (solo si son contactos mutuos)"""
    # Verificar que sean contactos mutuos
    if not Contact.are_contacts(current_user.id, user_id):
        flash('Solo puedes ver perfiles de tus contactos aceptados', 'error')
        return redirect(url_for('contacts.index'))
    
    user = User.find_by_id(user_id)
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('contacts.index'))
    
    # Mostrar solo redes sociales visibles
    social_links = SocialLink.get_visible_by_user(user_id)
    return render_template('profile/view.html', user=user, social_links=social_links, is_own_profile=False)

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

@bp.route('/social-links', methods=['GET'])
@login_required
def social_links():
    """Gestionar enlaces a redes sociales - Vista de ficha de contacto"""
    links = SocialLink.get_by_user(current_user.id)
    
    # Convertir lista de links a diccionario por plataforma
    links_dict = {}
    for link in links:
        links_dict[link['platform']] = link
    
    return render_template('profile/social_links.html', links=links, links_dict=links_dict)

@bp.route('/social-links/save', methods=['POST'])
@login_required
def save_social_link():
    """Guardar o actualizar enlace a red social"""
    platform = request.form.get('platform')
    username = request.form.get('username')
    url = request.form.get('url')
    is_visible = request.form.get('is_visible') == '1'
    
    if not url:
        flash(f'Por favor ingresa la URL de tu perfil de {platform}', 'error')
        return redirect(url_for('profile.my_profile'))
    
    # Extraer información del enlace
    try:
        extracted_data = extract_social_info(url, platform)
        
        # Si no se proporcionó username, usar el extraído
        username = extracted_data.get('username', '')
        
        # Si aún no hay username, usar un valor por defecto
        if not username:
            username = 'Mi perfil'
        
        # Guardar toda la info extraída como profile_data
        profile_data = extracted_data
        
    except Exception as e:
        print(f"Error extrayendo info: {str(e)}")
        # Si falla la extracción, usar valores básicos
        username = request.form.get('username', 'Mi perfil')
        profile_data = None
    
    # Verificar si ya existe este enlace
    existing = SocialLink.get_by_platform(current_user.id, platform)
    
    if existing:
        # Actualizar con profile_data
        SocialLink.update(existing['id'], current_user.id, username, url, is_visible, profile_data)
        flash(f'✅ {platform} actualizado correctamente', 'success')
    else:
        # Crear nuevo con profile_data
        SocialLink.create(current_user.id, platform, username, url, is_visible, profile_data)
        flash(f'✅ {platform} agregado correctamente', 'success')
    
    return redirect(url_for('profile.my_profile'))

@bp.route('/social-links/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_social_link(link_id):
    """Eliminar enlace a red social"""
    SocialLink.delete(link_id, current_user.id)
    flash('Red social eliminada', 'success')
    return redirect(url_for('profile.social_links'))
