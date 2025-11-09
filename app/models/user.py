"""Modelo de Usuario - MySQL directo"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app import login_manager

class User(UserMixin):
    """Usuario del sistema eID"""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None,
                 full_name=None, bio=None, avatar='default.png', website=None,
                 created_at=None, is_active=True):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.bio = bio
        self.avatar = avatar
        self.website = website
        self.created_at = created_at
        self.is_active = is_active
    
    @staticmethod
    def create(username, email, password, full_name=None):
        """Crear nuevo usuario"""
        password_hash = generate_password_hash(password)
        query = """
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (%s, %s, %s, %s)
        """
        user_id = db.execute_query(query, (username, email, password_hash, full_name))
        return user_id
    
    @staticmethod
    def find_by_id(user_id):
        """Buscar usuario por ID"""
        query = "SELECT * FROM users WHERE id = %s"
        row = db.fetch_one(query, (user_id,))
        if row:
            return User(**row)
        return None
    
    @staticmethod
    def find_by_username(username):
        """Buscar usuario por username"""
        query = "SELECT * FROM users WHERE username = %s"
        row = db.fetch_one(query, (username,))
        if row:
            return User(**row)
        return None
    
    @staticmethod
    def find_by_email(email):
        """Buscar usuario por email"""
        query = "SELECT * FROM users WHERE email = %s"
        row = db.fetch_one(query, (email,))
        if row:
            return User(**row)
        return None
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def update(self, full_name=None, bio=None, website=None):
        """Actualizar perfil"""
        query = """
            UPDATE users 
            SET full_name = %s, bio = %s, website = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        db.execute_query(query, (full_name, bio, website, self.id))
        self.full_name = full_name
        self.bio = bio
        self.website = website
    
    def get_social_links(self):
        """Obtener enlaces a redes sociales"""
        query = """
            SELECT * FROM social_links 
            WHERE user_id = %s AND is_visible = TRUE
            ORDER BY display_order
        """
        return db.fetch_all(query, (self.id,))
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    """Cargar usuario para Flask-Login"""
    return User.find_by_id(int(user_id))
