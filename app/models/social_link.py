"""Modelo de Enlaces a Redes Sociales - MySQL directo"""

from app.database import db

class SocialLink:
    """Enlaces a redes sociales del usuario"""
    
    @staticmethod
    def create(user_id, platform, username, url, icon=None):
        """Crear nuevo enlace"""
        query = """
            INSERT INTO social_links (user_id, platform, username, url, icon)
            VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(query, (user_id, platform, username, url, icon))
    
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
