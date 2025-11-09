"""
Modelo para carpetas de contactos
"""

from app.database import db

class ContactFolder:
    """Modelo de carpeta de contactos"""
    
    def __init__(self, id=None, user_id=None, name=None, color='#6366f1', 
                 icon='folder', position=0, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.color = color
        self.icon = icon
        self.position = position
        self.created_at = created_at
        self.updated_at = updated_at
    
    def save(self):
        """Guardar o actualizar carpeta"""
        if self.id:
            # Actualizar
            query = """
                UPDATE contact_folders 
                SET name = %s, color = %s, icon = %s, position = %s
                WHERE id = %s AND user_id = %s
            """
            db.execute_query(query, (self.name, self.color, self.icon, 
                                    self.position, self.id, self.user_id))
            return self.id
        else:
            # Crear nueva
            query = """
                INSERT INTO contact_folders (user_id, name, color, icon, position)
                VALUES (%s, %s, %s, %s, %s)
            """
            folder_id = db.execute_query(query, (self.user_id, self.name, 
                                                self.color, self.icon, self.position))
            self.id = folder_id
            return folder_id
    
    def delete(self):
        """Eliminar carpeta (los contactos quedan sin carpeta)"""
        query = "DELETE FROM contact_folders WHERE id = %s AND user_id = %s"
        db.execute_query(query, (self.id, self.user_id))
    
    def get_contacts_count(self):
        """Obtener número de contactos en esta carpeta"""
        query = """
            SELECT COUNT(*) as count
            FROM contacts
            WHERE user_id = %s AND folder_id = %s AND status = 'accepted'
        """
        result = db.fetch_one(query, (self.user_id, self.id))
        return result['count'] if result else 0
    
    @staticmethod
    def get_by_id(folder_id, user_id):
        """Obtener carpeta por ID"""
        query = "SELECT * FROM contact_folders WHERE id = %s AND user_id = %s"
        row = db.fetch_one(query, (folder_id, user_id))
        if row:
            return ContactFolder(**row)
        return None
    
    @staticmethod
    def get_all_by_user(user_id):
        """Obtener todas las carpetas de un usuario"""
        query = """
            SELECT * FROM contact_folders 
            WHERE user_id = %s 
            ORDER BY position ASC, name ASC
        """
        rows = db.fetch_all(query, (user_id,))
        folders = [ContactFolder(**row) for row in rows]
        
        # Añadir conteo de contactos a cada carpeta
        for folder in folders:
            folder.contacts_count = folder.get_contacts_count()
        
        return folders
    
    @staticmethod
    def create_default_folder(user_id):
        """Crear carpeta por defecto 'Todos' para un usuario nuevo"""
        folder = ContactFolder(
            user_id=user_id,
            name='Todos',
            color='#6366f1',
            icon='users',
            position=0
        )
        return folder.save()
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'color': self.color,
            'icon': self.icon,
            'position': self.position,
            'contacts_count': getattr(self, 'contacts_count', 0),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
