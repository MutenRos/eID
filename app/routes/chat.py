"""Rutas de chat/mensajería"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.user import User
from app.models.message import Message
from app.models.contact import Contact

bp = Blueprint('chat', __name__, url_prefix='/chat')

@bp.route('/')
@login_required
def index():
    """Lista de conversaciones"""
    # Obtener contactos aceptados
    contacts = Contact.get_accepted(current_user.id)
    
    return render_template('chat/index.html', contacts=contacts)

@bp.route('/<int:user_id>')
@login_required
def conversation(user_id):
    """Conversación con un usuario"""
    other_user = User.find_by_id(user_id)
    if not other_user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('chat.index'))
    
    # Verificar que sean contactos
    if not Contact.are_contacts(current_user.id, user_id):
        flash('No tienes contacto con este usuario', 'error')
        return redirect(url_for('chat.index'))
    
    # Obtener mensajes
    messages = Message.get_conversation(current_user.id, user_id)
    
    # Marcar como leídos los mensajes recibidos
    Message.mark_as_read(user_id, current_user.id)
    
    return render_template('chat/conversation.html', other_user=other_user, messages=messages)

@bp.route('/<int:user_id>/send', methods=['POST'])
@login_required
def send_message(user_id):
    """Enviar mensaje"""
    content = request.form.get('content', '').strip()
    
    if not content or len(content) == 0:
        flash('El mensaje no puede estar vacío', 'error')
        return redirect(url_for('chat.conversation', user_id=user_id))
    
    # Limitar longitud del mensaje a 2000 caracteres
    if len(content) > 2000:
        flash('El mensaje no puede superar los 2000 caracteres', 'error')
        return redirect(url_for('chat.conversation', user_id=user_id))
    
    Message.create(current_user.id, user_id, content)
    
    return redirect(url_for('chat.conversation', user_id=user_id))

@bp.route('/unread-count')
@login_required
def unread_count():
    """Cantidad de mensajes no leídos"""
    count = Message.count_unread(current_user.id)
    return jsonify({'count': count})
