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
    """Lista de contactos"""
    contacts = Contact.get_accepted(current_user.id)
    pending_sent = Contact.get_pending_sent(current_user.id)
    pending_received = Contact.get_pending_received(current_user.id)
    
    return render_template('contacts/index.html',
                         contacts=contacts,
                         pending_sent=pending_sent,
                         pending_received=pending_received)

@bp.route('/add/<int:user_id>', methods=['POST'])
@login_required
def add(user_id):
    """Enviar solicitud de contacto"""
    if user_id == current_user.id:
        flash('No puedes agregarte a ti mismo', 'error')
        return redirect(url_for('contacts.index'))
    
    # Verificar si ya existe la relación
    if Contact.exists(current_user.id, user_id):
        flash('Ya existe una solicitud con este usuario', 'error')
        return redirect(url_for('contacts.index'))
    
    Contact.create(current_user.id, user_id)
    flash('Solicitud de contacto enviada', 'success')
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

@bp.route('/search')
@login_required
def search():
    """Buscar usuarios"""
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify([])
    
    sql = """
        SELECT id, username, full_name, avatar
        FROM users
        WHERE (username LIKE %s OR full_name LIKE %s)
          AND id != %s
        LIMIT 10
    """
    search_term = f'%{query}%'
    users = db.fetch_all(sql, (search_term, search_term, current_user.id))
    
    return jsonify(users)
