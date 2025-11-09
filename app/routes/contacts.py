"""Rutas de agenda de contactos"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.contact import Contact

bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@bp.route('/')
@login_required
def index():
    """Lista de contactos"""
    contacts = Contact.query.filter_by(
        user_id=current_user.id,
        status='accepted'
    ).all()
    
    pending_sent = Contact.query.filter_by(
        user_id=current_user.id,
        status='pending'
    ).all()
    
    pending_received = Contact.query.filter_by(
        contact_id=current_user.id,
        status='pending'
    ).all()
    
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
    existing = Contact.query.filter_by(
        user_id=current_user.id,
        contact_id=user_id
    ).first()
    
    if existing:
        flash('Ya existe una solicitud con este usuario', 'error')
        return redirect(url_for('contacts.index'))
    
    contact = Contact(user_id=current_user.id, contact_id=user_id)
    db.session.add(contact)
    db.session.commit()
    
    flash('Solicitud de contacto enviada', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/accept/<int:contact_id>', methods=['POST'])
@login_required
def accept(contact_id):
    """Aceptar solicitud de contacto"""
    contact = Contact.query.get_or_404(contact_id)
    
    if contact.contact_id != current_user.id:
        flash('No autorizado', 'error')
        return redirect(url_for('contacts.index'))
    
    contact.status = 'accepted'
    db.session.commit()
    
    flash('Contacto aceptado', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/reject/<int:contact_id>', methods=['POST'])
@login_required
def reject(contact_id):
    """Rechazar solicitud de contacto"""
    contact = Contact.query.get_or_404(contact_id)
    
    if contact.contact_id != current_user.id:
        flash('No autorizado', 'error')
        return redirect(url_for('contacts.index'))
    
    db.session.delete(contact)
    db.session.commit()
    
    flash('Solicitud rechazada', 'success')
    return redirect(url_for('contacts.index'))

@bp.route('/search')
@login_required
def search():
    """Buscar usuarios"""
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return jsonify([])
    
    users = User.query.filter(
        (User.username.like(f'%{query}%')) |
        (User.full_name.like(f'%{query}%'))
    ).filter(User.id != current_user.id).limit(10).all()
    
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'full_name': u.full_name,
        'avatar': u.avatar
    } for u in users])
