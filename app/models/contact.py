"""Modelo de Contactos/Agenda"""

from app import db
from datetime import datetime

class Contact(db.Model):
    """Relación de contactos entre usuarios"""
    
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Estado de la relación
    status = db.Column(db.String(20), default='pending')  # pending, accepted, blocked
    
    # Metadatos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_at = db.Column(db.DateTime)
    
    # Constraints
    __table_args__ = (
        db.UniqueConstraint('user_id', 'contact_id', name='unique_contact'),
    )
    
    def __repr__(self):
        return f'<Contact {self.user_id} -> {self.contact_id} [{self.status}]>'
