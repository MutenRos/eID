"""Modelo de Enlaces a Redes Sociales - MySQL directo"""

import json
from app.database import db

class SocialLink:
    """Enlaces a redes sociales del usuario"""
    
    @staticmethod
    def create(user_id, platform, username, url, is_visible=True, profile_data=None):
        """Crear nuevo enlace"""
        query = """
            INSERT INTO social_links (user_id, platform, username, url, is_visible, profile_data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        profile_json = json.dumps(profile_data) if profile_data else None
        return db.execute_query(query, (user_id, platform, username, url, is_visible, profile_json))
    
    @staticmethod
    def update(link_id, user_id, username, url, is_visible=True, profile_data=None):
        """Actualizar enlace existente"""
        query = """
            UPDATE social_links 
            SET username = %s, url = %s, is_visible = %s, profile_data = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
        """
        profile_json = json.dumps(profile_data) if profile_data else None
        return db.execute_query(query, (username, url, is_visible, profile_json, link_id, user_id))
    
    @staticmethod
    def get_by_platform(user_id, platform):
        """Obtener enlace por plataforma"""
        query = """
            SELECT * FROM social_links 
            WHERE user_id = %s AND platform = %s
        """
        return db.fetch_one(query, (user_id, platform))
    
    @staticmethod
    def get_by_user(user_id):
        """Obtener todos los enlaces de un usuario"""
        query = """
            SELECT * FROM social_links 
            WHERE user_id = %s 
            ORDER BY display_order
        """
        return db.fetch_all(query, (user_id,))
    
    @staticmethod
    def get_visible_by_user(user_id):
        """Obtener enlaces visibles de un usuario"""
        query = """
            SELECT * FROM social_links 
            WHERE user_id = %s AND is_visible = TRUE
            ORDER BY display_order
        """
        return db.fetch_all(query, (user_id,))
    
    @staticmethod
    def delete(link_id, user_id):
        """Eliminar enlace (solo si pertenece al usuario)"""
        query = "DELETE FROM social_links WHERE id = %s AND user_id = %s"
        return db.execute_query(query, (link_id, user_id))
