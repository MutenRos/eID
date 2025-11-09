"""
eID - Meta Red Social
Tarjeta de visita digital con agregación de redes sociales
"""

from flask import Flask, g
from flask_login import LoginManager
from app.database import db
import os

# Inicialización de extensiones
login_manager = LoginManager()

def create_app():
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Inicializar Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Conectar a la base de datos al inicio de cada request
    @app.before_request
    def before_request():
        if not db.connection or not db.connection.is_connected():
            db.connect()
    
    # Cerrar conexión al final de cada request
    @app.teardown_request
    def teardown_request(exception=None):
        if hasattr(g, 'db_connection'):
            db.disconnect()
    
    # Registrar blueprints
    from app.routes import main, auth, profile, contacts, chat, oauth, calendar
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(contacts.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(oauth.bp)
    app.register_blueprint(calendar.bp)
    
    return app



