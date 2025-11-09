"""Rutas de agenda de contactos"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.models.contact import Contact
from app.models.contact_folder import ContactFolder
from app.database import db

bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@bp.route('/')
@login_required
def index():
    """Lista de contactos y código de amigo"""
    contacts = Contact.get_accepted(current_user.id)
    pending_sent = Contact.get_pending_sent(current_user.id)
    pending_received = Contact.get_pending_received(current_user.id)
    folders = ContactFolder.get_all_by_user(current_user.id)
    
    # Filtrar por carpeta si se especifica
    folder_id = request.args.get('folder')
    if folder_id:
        contacts = [c for c in contacts if str(c.folder_id) == folder_id]
    
    return render_template('contacts/index.html',
                         contacts=contacts,
                         pending_sent=pending_sent,
                         pending_received=pending_received,
                         folders=folders,
                         active_folder=folder_id,
                         friend_code=current_user.friend_code)

@bp.route('/add', methods=['POST'])
@login_required
def add():
    """Agregar contacto por código de amigo"""
    friend_code = request.form.get('friend_code', '').strip().upper()
    
    if not friend_code:
        flash('Por favor ingresa un código de amigo', 'error')
        return redirect(url_for('contacts.index'))
    
    # Buscar usuario por código
    user = User.find_by_friend_code(friend_code)
    
    if not user:
        flash('Código de amigo no válido', 'error')
        return redirect(url_for('contacts.index'))
    
    if user.id == current_user.id:
        flash('No puedes agregarte a ti mismo', 'error')
        return redirect(url_for('contacts.index'))
    
    # Verificar si ya existe la relación
    if Contact.exists(current_user.id, user.id):
        flash('Ya existe una solicitud con este usuario', 'error')
        return redirect(url_for('contacts.index'))
    
    Contact.create(current_user.id, user.id)
    flash(f'Solicitud enviada a {user.username}', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/accept/<int:contact_id>', methods=['POST'])
@login_required
def accept(contact_id):
    """Aceptar solicitud de contacto"""
    Contact.accept(contact_id, current_user.id)
    flash('Contacto aceptado', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/reject/<int:contact_id>', methods=['POST'])
@login_required
def reject(contact_id):
    """Rechazar solicitud de contacto"""
    Contact.reject(contact_id, current_user.id)
    flash('Solicitud rechazada', 'success')
    return redirect(url_for('contacts.index'))

# ===== RUTAS PARA CARPETAS =====

@bp.route('/folders/create', methods=['POST'])
@login_required
def create_folder():
    """Crear nueva carpeta"""
    data = request.get_json() if request.is_json else request.form
    
    name = data.get('name', '').strip()
    color = data.get('color', '#6366f1')
    icon = data.get('icon', 'folder')
    
    if not name:
        if request.is_json:
            return jsonify({'error': 'Nombre requerido'}), 400
        flash('El nombre de la carpeta es requerido', 'error')
        return redirect(url_for('contacts.index'))
    
    folder = ContactFolder(
        user_id=current_user.id,
        name=name,
        color=color,
        icon=icon
    )
    folder.save()
    
    if request.is_json:
        return jsonify(folder.to_dict()), 201
    
    flash(f'Carpeta "{name}" creada exitosamente', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/folders/<int:folder_id>/edit', methods=['POST', 'PUT'])
@login_required
def edit_folder(folder_id):
    """Editar carpeta existente"""
    folder = ContactFolder.get_by_id(folder_id, current_user.id)
    
    if not folder:
        if request.is_json:
            return jsonify({'error': 'Carpeta no encontrada'}), 404
        flash('Carpeta no encontrada', 'error')
        return redirect(url_for('contacts.index'))
    
    data = request.get_json() if request.is_json else request.form
    
    folder.name = data.get('name', folder.name).strip()
    folder.color = data.get('color', folder.color)
    folder.icon = data.get('icon', folder.icon)
    folder.save()
    
    if request.is_json:
        return jsonify(folder.to_dict())
    
    flash('Carpeta actualizada', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/folders/<int:folder_id>/delete', methods=['POST', 'DELETE'])
@login_required
def delete_folder(folder_id):
    """Eliminar carpeta"""
    folder = ContactFolder.get_by_id(folder_id, current_user.id)
    
    if not folder:
        if request.is_json:
            return jsonify({'error': 'Carpeta no encontrada'}), 404
        flash('Carpeta no encontrada', 'error')
        return redirect(url_for('contacts.index'))
    
    folder.delete()
    
    if request.is_json:
        return jsonify({'message': 'Carpeta eliminada'}), 200
    
    flash('Carpeta eliminada', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/move-to-folder', methods=['POST'])
@login_required
def move_to_folder():
    """Mover contacto a una carpeta"""
    data = request.get_json() if request.is_json else request.form
    
    contact_id = data.get('contact_id')
    folder_id = data.get('folder_id')  # None para remover de carpeta
    
    if not contact_id:
        if request.is_json:
            return jsonify({'error': 'contact_id requerido'}), 400
        flash('Contacto no especificado', 'error')
        return redirect(url_for('contacts.index'))
    
    # Verificar que el contacto pertenece al usuario
    query = """
        UPDATE contacts 
        SET folder_id = %s 
        WHERE id = %s AND user_id = %s
    """
    db.execute_query(query, (folder_id, contact_id, current_user.id))
    
    if request.is_json:
        return jsonify({'message': 'Contacto movido exitosamente'})
    
    flash('Contacto movido a la carpeta', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/folders/list', methods=['GET'])
@login_required
def list_folders():
    """API: Obtener lista de carpetas del usuario"""
    folders = ContactFolder.get_all_by_user(current_user.id)
    return jsonify([folder.to_dict() for folder in folders])

