"""Modelo de Usuario - MySQL directo"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app import login_manager
import secrets
import string

class User(UserMixin):
    """Usuario del sistema eID"""
    
    def __init__(self, id=None, username=None, email=None, password_hash=None,
                 friend_code=None, full_name=None, bio=None, avatar='default.png', website=None,
                 google_id=None, oauth_provider=None,
                 created_at=None, updated_at=None, **kwargs):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.friend_code = friend_code
        self.full_name = full_name
        self.bio = bio
        self.avatar = avatar
        self.website = website
        self.google_id = google_id
        self.oauth_provider = oauth_provider
        self.created_at = created_at
        self.updated_at = updated_at
        # is_active viene de UserMixin, ignoramos si viene de la BD
    
    @staticmethod
    def generate_friend_code():
        """Generar código de amigo único (8 caracteres)"""
        while True:
            chars = string.ascii_uppercase + string.digits
            code = ''.join(secrets.choice(chars) for _ in range(8))
            # Verificar que sea único
            if not User.find_by_friend_code(code):
                return code
    
    @staticmethod
    def create(username, email, password, full_name=None):
        """Crear nuevo usuario"""
        password_hash = generate_password_hash(password)
        friend_code = User.generate_friend_code()
        query = """
            INSERT INTO users (username, email, password_hash, friend_code, full_name)
            VALUES (%s, %s, %s, %s, %s)
        """
        user_id = db.execute_query(query, (username, email, password_hash, friend_code, full_name))
        return user_id
    
    @staticmethod
    def create_with_google(google_id, email, full_name=None):
        """Crear usuario con Google OAuth"""
        # Generar username a partir del email
        username = email.split('@')[0]
        # Asegurar que sea único
        base_username = username
        counter = 1
        while User.find_by_username(username):
            username = f"{base_username}{counter}"
            counter += 1
        
        friend_code = User.generate_friend_code()
        query = """
            INSERT INTO users (username, email, friend_code, full_name, google_id, oauth_provider)
            VALUES (%s, %s, %s, %s, %s, 'google')
        """
        user_id = db.execute_query(query, (username, email, friend_code, full_name, google_id))
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
    
    @staticmethod
    def find_by_friend_code(friend_code):
        """Buscar usuario por código de amigo"""
        query = "SELECT * FROM users WHERE friend_code = %s"
        row = db.fetch_one(query, (friend_code,))
        if row:
            return User(**row)
        return None
    
    @staticmethod
    def find_by_google_id(google_id):
        """Buscar usuario por Google ID"""
        query = "SELECT * FROM users WHERE google_id = %s"
        row = db.fetch_one(query, (google_id,))
        if row:
            return User(**row)
        return None
    
    def check_password(self, password):
        """Verificar contraseña"""
        # Si es usuario OAuth, no tiene contraseña
        if not self.password_hash:
            return False
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
    
    def link_google_account(self, google_id):
        """Vincular cuenta existente con Google"""
        query = """
            UPDATE users 
            SET google_id = %s, oauth_provider = 'google'
            WHERE id = %s
        """
        db.execute_query(query, (google_id, self.id))
        self.google_id = google_id
        self.oauth_provider = 'google'
    
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
