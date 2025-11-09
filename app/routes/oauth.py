"""Rutas para autenticación OAuth con redes sociales"""

from flask import Blueprint, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from app.oauth_config import get_oauth_config, OAUTH_CONFIGS
from app.models.social_link import SocialLink
import requests
import secrets

bp = Blueprint('oauth', __name__, url_prefix='/oauth')

@bp.route('/connect/<platform>')
@login_required
def connect(platform):
    """Iniciar flujo OAuth para conectar una red social"""
    provider, config = get_oauth_config(platform)
    
    if not config or not config['client_id']:
        flash(f'La integración con {platform} no está configurada aún', 'error')
        return redirect(url_for('profile.my_profile'))
    
    # Generar estado para CSRF protection
    state = secrets.token_urlsafe(32)
    session[f'oauth_state_{platform}'] = state
    session[f'oauth_platform'] = platform
    
    # Construir URL de autorización
    redirect_uri = url_for('oauth.callback', platform=platform, _external=True)
    
    params = {
        'client_id': config['client_id'],
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': config['scope'],
        'state': state
    }
    
    # Parámetros específicos por plataforma
    if provider == 'google':
        params['access_type'] = 'offline'
        params['prompt'] = 'consent'
    elif provider == 'facebook':
        params['display'] = 'popup'
    
    auth_url = config['authorize_url'] + '?' + '&'.join([f'{k}={v}' for k, v in params.items()])
    
    return redirect(auth_url)

@bp.route('/callback/<platform>')
@login_required
def callback(platform):
    """Callback después de autorización OAuth"""
    provider, config = get_oauth_config(platform)
    
    if not config:
        flash(f'Error en la configuración de {platform}', 'error')
        return redirect(url_for('profile.my_profile'))
    
    # Verificar estado CSRF
    state = request.args.get('state')
    expected_state = session.get(f'oauth_state_{platform}')
    
    if not state or state != expected_state:
        flash('Error de seguridad en la autenticación', 'error')
        return redirect(url_for('profile.my_profile'))
    
    # Verificar si hubo error
    error = request.args.get('error')
    if error:
        flash(f'Error al conectar con {platform}: {error}', 'error')
        return redirect(url_for('profile.my_profile'))
    
    # Obtener código de autorización
    code = request.args.get('code')
    if not code:
        flash('No se recibió código de autorización', 'error')
        return redirect(url_for('profile.my_profile'))
    
    # Intercambiar código por token
    redirect_uri = url_for('oauth.callback', platform=platform, _external=True)
    
    token_data = {
        'client_id': config['client_id'],
        'client_secret': config['client_secret'],
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    
    try:
        # Obtener access token
        token_response = requests.post(config['token_url'], data=token_data)
        token_response.raise_for_status()
        token_info = token_response.json()
        access_token = token_info.get('access_token')
        
        if not access_token:
            flash('No se pudo obtener el token de acceso', 'error')
            return redirect(url_for('profile.my_profile'))
        
        # Obtener información del usuario
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(config['userinfo_url'], headers=headers)
        user_response.raise_for_status()
        user_info = user_response.json()
        
        # Extraer datos según la plataforma
        username, profile_url = extract_platform_data(platform, provider, user_info, access_token)
        
        if not username or not profile_url:
            flash(f'No se pudo obtener tu información de {platform}', 'error')
            return redirect(url_for('profile.my_profile'))
        
        # Guardar en la base de datos
        existing = SocialLink.get_by_platform(current_user.id, platform)
        
        if existing:
            SocialLink.update(existing['id'], current_user.id, username, profile_url, True)
            flash(f'✅ {platform} actualizado correctamente: @{username}', 'success')
        else:
            SocialLink.create(current_user.id, platform, username, profile_url, True)
            flash(f'✅ {platform} conectado correctamente: @{username}', 'success')
        
        # Limpiar session
        session.pop(f'oauth_state_{platform}', None)
        session.pop('oauth_platform', None)
        
        return redirect(url_for('profile.my_profile'))
        
    except requests.exceptions.RequestException as e:
        flash(f'Error al conectar con {platform}: {str(e)}', 'error')
        return redirect(url_for('profile.my_profile'))

def extract_platform_data(platform, provider, user_info, access_token):
    """Extraer username y URL según la plataforma"""
    username = None
    profile_url = None
    
    if provider == 'google':
        # Para YouTube
        username = user_info.get('name') or user_info.get('email').split('@')[0]
        # Necesitaríamos hacer otra llamada a YouTube API para obtener el canal
        channel_id = get_youtube_channel_id(access_token)
        if channel_id:
            profile_url = f'https://youtube.com/channel/{channel_id}'
        else:
            profile_url = f'https://youtube.com/@{username}'
    
    elif provider == 'facebook':
        if platform == 'Facebook':
            username = user_info.get('name')
            user_id = user_info.get('id')
            profile_url = f'https://facebook.com/{user_id}'
        elif platform == 'Instagram':
            # Instagram requiere permisos adicionales
            username = user_info.get('username', user_info.get('name'))
            profile_url = f'https://instagram.com/{username}'
    
    elif provider == 'twitter':
        username = user_info.get('data', {}).get('username')
        profile_url = f'https://x.com/{username}'
    
    elif provider == 'linkedin':
        # LinkedIn usa un formato diferente
        first_name = user_info.get('localizedFirstName', '')
        last_name = user_info.get('localizedLastName', '')
        username = f'{first_name} {last_name}'.strip()
        # LinkedIn no proporciona URL pública fácilmente, usamos el ID
        profile_url = f'https://linkedin.com/in/{username.lower().replace(" ", "-")}'
    
    elif provider == 'tiktok':
        data = user_info.get('data', {}).get('user', {})
        username = data.get('display_name')
        unique_id = data.get('unique_id')
        profile_url = f'https://tiktok.com/@{unique_id}'
    
    return username, profile_url

def get_youtube_channel_id(access_token):
    """Obtener ID del canal de YouTube"""
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/channels',
            headers=headers,
            params={'part': 'id', 'mine': 'true'}
        )
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])
        if items:
            return items[0]['id']
    except:
        pass
    return None
