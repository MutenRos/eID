"""Modelo de Mensajes/Chat - MySQL directo"""

from app.database import db

class Message:
    """Mensajes entre usuarios"""
    
    @staticmethod
    def create(sender_id, receiver_id, content):
        """Crear nuevo mensaje"""
        query = """
            INSERT INTO messages (sender_id, receiver_id, content)
            VALUES (%s, %s, %s)
        """
        return db.execute_query(query, (sender_id, receiver_id, content))
    
    @staticmethod
    def get_conversation(user1_id, user2_id):
        """Obtener conversación entre dos usuarios"""
        query = """
            SELECT * FROM messages
            WHERE (sender_id = %s AND receiver_id = %s)
               OR (sender_id = %s AND receiver_id = %s)
            ORDER BY created_at ASC
        """
        return db.fetch_all(query, (user1_id, user2_id, user2_id, user1_id))
    
    @staticmethod
    def mark_as_read(sender_id, receiver_id):
        """Marcar mensajes como leídos"""
        query = """
            UPDATE messages 
            SET is_read = TRUE, read_at = CURRENT_TIMESTAMP
            WHERE sender_id = %s AND receiver_id = %s AND is_read = FALSE
        """
        return db.execute_query(query, (sender_id, receiver_id))
    
    @staticmethod
    def count_unread(user_id):
        """Contar mensajes no leídos"""
        query = """
            SELECT COUNT(*) as count FROM messages
            WHERE receiver_id = %s AND is_read = FALSE
        """
        result = db.fetch_one(query, (user_id,))
        return result['count'] if result else 0
