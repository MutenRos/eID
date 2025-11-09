"""Rutas de agenda de contactos"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.models.contact import Contact
from app.database import db

bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@bp.route('/')
@login_required
def index():
    """Lista de contactos y código de amigo"""
    contacts = Contact.get_accepted(current_user.id)
    pending_sent = Contact.get_pending_sent(current_user.id)
    pending_received = Contact.get_pending_received(current_user.id)
    
    return render_template('contacts/index.html',
                         contacts=contacts,
                         pending_sent=pending_sent,
                         pending_received=pending_received,
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
