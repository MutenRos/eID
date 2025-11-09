"""Modelo de Enlaces a Redes Sociales"""

from app import db
from datetime import datetime

class SocialLink(db.Model):
    """Enlaces a redes sociales del usuario"""
    
    __tablename__ = 'social_links'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Datos de la red social
    platform = db.Column(db.String(50), nullable=False)  # twitter, instagram, linkedin, github, etc
    username = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    icon = db.Column(db.String(50))  # Clase CSS del icono
    
    # Configuración
    is_visible = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SocialLink {self.platform}: {self.username}>'
