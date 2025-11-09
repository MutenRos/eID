"""Modelo de Contactos/Agenda - MySQL directo"""

from app.database import db

class Contact:
    """Relación de contactos entre usuarios"""
    
    @staticmethod
    def create(user_id, contact_id):
        """Crear solicitud de contacto"""
        query = """
            INSERT INTO contacts (user_id, contact_id, status)
            VALUES (%s, %s, 'pending')
        """
        return db.execute_query(query, (user_id, contact_id))
    
    @staticmethod
    def exists(user_id, contact_id):
        """Verificar si ya existe la relación"""
        query = """
            SELECT id FROM contacts 
            WHERE (user_id = %s AND contact_id = %s) 
               OR (user_id = %s AND contact_id = %s)
        """
        return db.fetch_one(query, (user_id, contact_id, contact_id, user_id))
    
    @staticmethod
    def get_accepted(user_id):
        """Obtener contactos aceptados"""
        query = """
            SELECT c.*, u.username, u.full_name, u.avatar
            FROM contacts c
            JOIN users u ON (
                CASE 
                    WHEN c.user_id = %s THEN u.id = c.contact_id
                    ELSE u.id = c.user_id
                END
            )
            WHERE (c.user_id = %s OR c.contact_id = %s) 
              AND c.status = 'accepted'
        """
        return db.fetch_all(query, (user_id, user_id, user_id))
    
    @staticmethod
    def get_pending_sent(user_id):
        """Obtener solicitudes enviadas pendientes"""
        query = """
            SELECT c.*, u.username, u.full_name
            FROM contacts c
            JOIN users u ON u.id = c.contact_id
            WHERE c.user_id = %s AND c.status = 'pending'
        """
        return db.fetch_all(query, (user_id,))
    
    @staticmethod
    def get_pending_received(user_id):
        """Obtener solicitudes recibidas pendientes"""
        query = """
            SELECT c.*, u.username, u.full_name
            FROM contacts c
            JOIN users u ON u.id = c.user_id
            WHERE c.contact_id = %s AND c.status = 'pending'
        """
        return db.fetch_all(query, (user_id,))
    
    @staticmethod
    def accept(contact_id, user_id):
        """Aceptar solicitud de contacto"""
        query = """
            UPDATE contacts 
            SET status = 'accepted', accepted_at = CURRENT_TIMESTAMP
            WHERE id = %s AND contact_id = %s
        """
        return db.execute_query(query, (contact_id, user_id))
    
    @staticmethod
    def reject(contact_id, user_id):
        """Rechazar/eliminar solicitud"""
        query = "DELETE FROM contacts WHERE id = %s AND contact_id = %s"
        return db.execute_query(query, (contact_id, user_id))
    
    @staticmethod
    def are_contacts(user1_id, user2_id):
        """Verificar si dos usuarios son contactos"""
        query = """
            SELECT id FROM contacts 
            WHERE ((user_id = %s AND contact_id = %s) 
               OR (user_id = %s AND contact_id = %s))
              AND status = 'accepted'
        """
        return db.fetch_one(query, (user1_id, user2_id, user2_id, user1_id))
