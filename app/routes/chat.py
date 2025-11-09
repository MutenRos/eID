"""Rutas de chat/mensajería"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.message import Message
from app.models.contact import Contact
from datetime import datetime
from sqlalchemy import or_, and_

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/')
@login_required
def index():
    """Lista de conversaciones"""
    # Obtener contactos aceptados
    contacts = Contact.query.filter(
        or_(
            and_(Contact.user_id == current_user.id, Contact.status == 'accepted'),
            and_(Contact.contact_id == current_user.id, Contact.status == 'accepted')
        )
    ).all()
    
    return render_template('chat/index.html', contacts=contacts)

@bp.route('/<int:user_id>')
@login_required
def conversation(user_id):
    """Conversación con un usuario"""
    other_user = User.query.get_or_404(user_id)
    
    # Verificar que sean contactos
    contact = Contact.query.filter(
        or_(
            and_(Contact.user_id == current_user.id, Contact.contact_id == user_id),
            and_(Contact.user_id == user_id, Contact.contact_id == current_user.id)
        ),
        Contact.status == 'accepted'
    ).first()
    
    if not contact:
        flash('No tienes contacto con este usuario', 'error')
        return redirect(url_for('chat.index'))
    
    # Obtener mensajes
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at).all()
    
    # Marcar como leídos los mensajes recibidos
    unread = Message.query.filter_by(
        sender_id=user_id,
        receiver_id=current_user.id,
        is_read=False
    ).all()
    
    for msg in unread:
        msg.is_read = True
        msg.read_at = datetime.utcnow()
    
    db.session.commit()
    
    return render_template('chat/conversation.html', other_user=other_user, messages=messages)

@bp.route('/<int:user_id>/send', methods=['POST'])
@login_required
def send_message(user_id):
    """Enviar mensaje"""
    content = request.form.get('content')
    
    if not content or len(content.strip()) == 0:
        flash('El mensaje no puede estar vacío', 'error')
        return redirect(url_for('chat.conversation', user_id=user_id))
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=user_id,
        content=content
    )
    
    db.session.add(message)
    db.session.commit()
    
    return redirect(url_for('chat.conversation', user_id=user_id))

@bp.route('/unread-count')
@login_required
def unread_count():
    """Cantidad de mensajes no leídos"""
    count = Message.query.filter_by(
        receiver_id=current_user.id,
        is_read=False
    ).count()
    
    return jsonify({'count': count})
