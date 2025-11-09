"""
Extractor de información de URLs de redes sociales
Sin usar APIs - solo parsing de URLs y scraping básico
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def extract_social_info(url, platform):
    """
    Extrae información de una URL de red social
    Retorna: dict con información extraída
    """
    try:
        # Normalizar URL
        if not url.startswith('http'):
            url = 'https://' + url
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.strip('/')
        
        info = {
            'url': url,
            'platform': platform,
            'username': None,
            'profile_name': None,
            'avatar': None,
            'bio': None,
            'followers': None,
            'verified': False,
            'additional_info': {}
        }
        
        # Extraer username de la URL según la plataforma
        if 'instagram.com' in domain:
            info.update(_extract_instagram(url, path))
        elif 'facebook.com' in domain or 'fb.com' in domain:
            info.update(_extract_facebook(url, path))
        elif 'twitter.com' in domain or 'x.com' in domain:
            info.update(_extract_twitter(url, path))
        elif 'linkedin.com' in domain:
            info.update(_extract_linkedin(url, path))
        elif 'tiktok.com' in domain:
            info.update(_extract_tiktok(url, path))
        elif 'youtube.com' in domain or 'youtu.be' in domain:
            info.update(_extract_youtube(url, path, parsed))
        elif 'wa.me' in domain or 'whatsapp.com' in domain:
            info.update(_extract_whatsapp(url, path))
        
        # Intentar scraping básico para obtener más info
        info = _scrape_basic_info(url, info)
        
        return info
        
    except Exception as e:
        print(f"Error extrayendo info de {url}: {str(e)}")
        return {'url': url, 'platform': platform, 'error': str(e)}


def _extract_instagram(url, path):
    """Extrae info de Instagram desde la URL"""
    # Patrón: instagram.com/username o instagram.com/p/POST_ID
    match = re.match(r'^([^/]+)/?', path)
    username = match.group(1) if match else None
    
    # Limpiar username
    if username and not username.startswith('p/'):
        username = username.replace('@', '')
        return {'username': f'@{username}'}
    return {'username': None}


def _extract_facebook(url, path):
    """Extrae info de Facebook desde la URL"""
    # Patrones: facebook.com/username, facebook.com/profile.php?id=123
    if 'profile.php' in url:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        user_id = params.get('id', [None])[0]
        return {'username': f'ID: {user_id}' if user_id else None}
    else:
        match = re.match(r'^([^/]+)/?', path)
        username = match.group(1) if match else None
        return {'username': username}


def _extract_twitter(url, path):
    """Extrae info de Twitter/X desde la URL"""
    # Patrón: twitter.com/username o x.com/username
    match = re.match(r'^([^/]+)/?', path)
    username = match.group(1) if match else None
    if username:
        return {'username': f'@{username}'}
    return {'username': None}


def _extract_linkedin(url, path):
    """Extrae info de LinkedIn desde la URL"""
    # Patrón: linkedin.com/in/username
    match = re.search(r'/in/([^/]+)', path)
    username = match.group(1) if match else None
    return {'username': username}


def _extract_tiktok(url, path):
    """Extrae info de TikTok desde la URL"""
    # Patrón: tiktok.com/@username
    match = re.match(r'@?([^/]+)/?', path)
    username = match.group(1) if match else None
    if username:
        return {'username': f'@{username}'}
    return {'username': None}


def _extract_youtube(url, path, parsed):
    """Extrae info de YouTube desde la URL"""
    # Patrones: youtube.com/@username, youtube.com/c/channel, youtube.com/channel/ID
    if '@' in path:
        match = re.search(r'@([^/]+)', path)
        username = match.group(1) if match else None
        return {'username': f'@{username}'}
    elif '/c/' in path:
        match = re.search(r'/c/([^/]+)', path)
        channel = match.group(1) if match else None
        return {'username': channel}
    elif '/channel/' in path:
        match = re.search(r'/channel/([^/]+)', path)
        channel_id = match.group(1) if match else None
        return {'username': channel_id, 'additional_info': {'channel_id': channel_id}}
    return {'username': None}


def _extract_whatsapp(url, path):
    """Extrae info de WhatsApp desde la URL"""
    # Patrón: wa.me/34600000000
    phone = path.replace('/', '')
    if phone:
        # Formatear número de teléfono
        if phone.startswith('34'):
            formatted = f'+34 {phone[2:5]} {phone[5:8]} {phone[8:]}'
        else:
            formatted = f'+{phone}'
        return {'username': formatted, 'additional_info': {'phone': phone}}
    return {'username': None}


def _scrape_basic_info(url, info):
    """
    Intenta hacer scraping básico de la página para obtener más información
    NOTA: Muchas redes sociales bloquean scraping o requieren JS
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Timeout corto para no bloquear la UI
        response = requests.get(url, headers=headers, timeout=3, allow_redirects=True)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Intentar extraer meta tags comunes
            og_title = soup.find('meta', property='og:title')
            if og_title:
                info['profile_name'] = og_title.get('content', '')
            
            og_description = soup.find('meta', property='og:description')
            if og_description:
                info['bio'] = og_description.get('content', '')[:200]  # Limitar a 200 chars
            
            og_image = soup.find('meta', property='og:image')
            if og_image:
                info['avatar'] = og_image.get('content', '')
            
            # Título de la página como fallback
            if not info.get('profile_name'):
                title = soup.find('title')
                if title:
                    info['profile_name'] = title.string
        
        return info
        
    except requests.exceptions.Timeout:
        # No bloquear si el scraping tarda mucho
        info['scraping_note'] = 'Timeout al obtener información adicional'
        return info
    except Exception as e:
        # No fallar si el scraping no funciona
        info['scraping_note'] = f'No se pudo obtener información adicional: {str(e)}'
        return info


def format_social_preview(info):
    """
    Formatea la información extraída para mostrar en HTML
    """
    html = f"""
    <div class="social-preview">
        <div class="preview-header">
            {f'<img src="{info.get("avatar")}" alt="Avatar" class="preview-avatar">' if info.get('avatar') else ''}
            <div class="preview-info">
                <h4>{info.get('profile_name') or info.get('username') or 'Perfil'}</h4>
                <p class="preview-username">{info.get('username', '')}</p>
            </div>
        </div>
        {f'<p class="preview-bio">{info.get("bio")}</p>' if info.get('bio') else ''}
        {f'<p class="preview-followers">👥 {info.get("followers")} seguidores</p>' if info.get('followers') else ''}
        <a href="{info['url']}" target="_blank" class="preview-link">Ver perfil completo →</a>
    </div>
    """
    return html
