"""Modelo de Mensajes/Chat"""

from app import db
from datetime import datetime

class Message(db.Model):
    """Mensajes entre usuarios"""
    
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Contenido
    content = db.Column(db.Text, nullable=False)
    
    # Estado
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Message {self.sender_id} -> {self.receiver_id}>'
