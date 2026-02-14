"""Rutas de autenticación"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
import requests
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registro de usuario"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        # Validar longitud mínima de contraseña
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return redirect(url_for('auth.register'))
        
        # Validar formato de username (solo letras, números y guiones)
        import re
        if not re.match(r'^[a-zA-Z0-9_-]{3,30}$', username):
            flash('El nombre de usuario solo puede tener letras, números, guiones y de 3 a 30 caracteres', 'error')
            return redirect(url_for('auth.register'))
        
        # Validaciones
        if User.find_by_username(username):
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('auth.register'))
        
        if User.find_by_email(email):
            flash('El email ya está registrado', 'error')
            return redirect(url_for('auth.register'))
        
        # Crear usuario
        user_id = User.create(username, email, password)
        
        if user_id:
            flash('Registro exitoso. Ya puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Error al crear el usuario', 'error')
            return redirect(url_for('auth.register'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesión"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        link_google = request.form.get('link_google')
        
        # Intentar buscar por username o email
        user = User.find_by_username(username)
        if not user:
            user = User.find_by_email(username)
        
        if user and user.check_password(password):
            login_user(user)
            
            # Si hay un Google ID pendiente de vincular, hacerlo ahora
            if link_google and session.get('link_google_id'):
                google_id = session.get('link_google_id')
                google_email = session.get('link_google_email')
                
                # Verificar que el email coincida
                if user.email == google_email:
                    user.link_google_account(google_id)
                    flash('✅ Tu cuenta ha sido vinculada con Google exitosamente', 'success')
                    session.pop('link_google_id', None)
                    session.pop('link_google_email', None)
                    session.pop('link_google_name', None)
                else:
                    flash('El email de tu cuenta no coincide con el de Google', 'error')
            
            next_page = request.args.get('next')
            return redirect(next_page or url_for('profile.my_profile'))
        
        flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('main.index'))

@bp.route('/google/login')
def google_login():
    """Iniciar login con Google"""
    # Generar state para CSRF
    state = secrets.token_urlsafe(32)
    session['google_auth_state'] = state
    
    # URL de autorización de Google
    authorize_url = 'https://accounts.google.com/o/oauth2/v2/auth'
    redirect_uri = url_for('auth.google_callback', _external=True)
    
    params = {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'online',
        'prompt': 'select_account'
    }
    
    auth_url = f"{authorize_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(auth_url)

@bp.route('/google/callback')
def google_callback():
    """Callback de Google OAuth"""
    # Verificar state
    state = request.args.get('state')
    if not state or state != session.get('google_auth_state'):
        flash('Error de seguridad en la autenticación', 'error')
        return redirect(url_for('auth.login'))
    
    # Limpiar state
    session.pop('google_auth_state', None)
    
    # Obtener código
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        flash(f'Error en la autenticación: {error}', 'error')
        return redirect(url_for('auth.login'))
    
    if not code:
        flash('No se recibió código de autorización', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        # Intercambiar código por token
        token_url = 'https://oauth2.googleapis.com/token'
        redirect_uri = url_for('auth.google_callback', _external=True)
        
        token_data = {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        token_info = token_response.json()
        access_token = token_info.get('access_token')
        
        if not access_token:
            flash('No se pudo obtener el token de acceso', 'error')
            return redirect(url_for('auth.login'))
        
        # Obtener información del usuario
        userinfo_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(userinfo_url, headers=headers)
        user_response.raise_for_status()
        user_info = user_response.json()
        
        google_id = user_info.get('id')
        email = user_info.get('email')
        full_name = user_info.get('name')
        
        if not google_id or not email:
            flash('No se pudo obtener tu información de Google', 'error')
            return redirect(url_for('auth.login'))
        
        # Buscar o crear usuario
        user = User.find_by_google_id(google_id)
        
        if not user:
            # Verificar si el email ya existe
            existing_user = User.find_by_email(email)
            if existing_user:
                # Si el usuario ya tiene Google ID, no debería estar aquí
                if existing_user.google_id:
                    flash('Esta cuenta de Google ya está vinculada.', 'error')
                    return redirect(url_for('auth.login'))
                
                # Ofrecer vincular la cuenta
                session['link_google_id'] = google_id
                session['link_google_email'] = email
                session['link_google_name'] = full_name
                flash(f'Ya existe una cuenta con el email {email}. Inicia sesión para vincular tu cuenta de Google.', 'info')
                return redirect(url_for('auth.login'))
            
            # Crear nuevo usuario
            user_id = User.create_with_google(google_id, email, full_name)
            user = User.find_by_id(user_id)
            flash(f'¡Bienvenido a eID, {full_name}! Tu cuenta ha sido creada.', 'success')
        else:
            flash(f'¡Bienvenido de nuevo, {user.full_name or user.username}!', 'success')
        
        # Iniciar sesión
        login_user(user)
        return redirect(url_for('profile.my_profile'))
        
    except requests.exceptions.RequestException as e:
        flash(f'Error al conectar con Google: {str(e)}', 'error')
        return redirect(url_for('auth.login'))

@bp.route('/link-google', methods=['POST'])
@login_required
def link_google():
    """Vincular cuenta actual con Google desde el perfil"""
    google_id = session.get('link_google_id')
    
    if not google_id:
        flash('No hay ninguna cuenta de Google pendiente de vincular', 'error')
        return redirect(url_for('profile.my_profile'))
    
    # Verificar que el Google ID no esté ya vinculado
    existing = User.find_by_google_id(google_id)
    if existing:
        flash('Esta cuenta de Google ya está vinculada a otro usuario', 'error')
        session.pop('link_google_id', None)
        session.pop('link_google_email', None)
        session.pop('link_google_name', None)
        return redirect(url_for('profile.my_profile'))
    
    # Vincular
    current_user.link_google_account(google_id)
    session.pop('link_google_id', None)
    session.pop('link_google_email', None)
    session.pop('link_google_name', None)
    
    flash('✅ Tu cuenta ha sido vinculada con Google. Ahora puedes iniciar sesión con Google.', 'success')
    return redirect(url_for('profile.my_profile'))
