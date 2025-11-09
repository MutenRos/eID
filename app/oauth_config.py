"""Configuración de OAuth para redes sociales"""

import os
from dotenv import load_dotenv

# Recargar variables de entorno
load_dotenv(override=True)

# Configuración de OAuth por plataforma
OAUTH_CONFIGS = {
    'google': {
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'authorize_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'userinfo_url': 'https://www.googleapis.com/oauth2/v2/userinfo',
        'scope': 'openid email profile https://www.googleapis.com/auth/youtube.readonly',
        'platforms': ['YouTube']  # Google OAuth sirve para YouTube
    },
    'facebook': {
        'client_id': os.getenv('FACEBOOK_APP_ID'),
        'client_secret': os.getenv('FACEBOOK_APP_SECRET'),
        'authorize_url': 'https://www.facebook.com/v18.0/dialog/oauth',
        'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token',
        'userinfo_url': 'https://graph.facebook.com/me',
        'scope': 'public_profile,email',
        'platforms': ['Facebook']
    },
    'instagram': {
        'client_id': os.getenv('INSTAGRAM_APP_ID'),
        'client_secret': os.getenv('INSTAGRAM_APP_SECRET'),
        'authorize_url': 'https://api.instagram.com/oauth/authorize',
        'token_url': 'https://api.instagram.com/oauth/access_token',
        'userinfo_url': 'https://graph.instagram.com/me',
        'scope': 'user_profile,user_media',
        'platforms': ['Instagram']
    },
    'twitter': {
        'client_id': os.getenv('TWITTER_CLIENT_ID'),
        'client_secret': os.getenv('TWITTER_CLIENT_SECRET'),
        'authorize_url': 'https://twitter.com/i/oauth2/authorize',
        'token_url': 'https://api.twitter.com/2/oauth2/token',
        'userinfo_url': 'https://api.twitter.com/2/users/me',
        'scope': 'tweet.read users.read',
        'platforms': ['X']
    },
    'linkedin': {
        'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
        'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET'),
        'authorize_url': 'https://www.linkedin.com/oauth/v2/authorization',
        'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
        'userinfo_url': 'https://api.linkedin.com/v2/me',
        'scope': 'r_liteprofile r_emailaddress',
        'platforms': ['LinkedIn']
    },
    'tiktok': {
        'client_id': os.getenv('TIKTOK_CLIENT_KEY'),
        'client_secret': os.getenv('TIKTOK_CLIENT_SECRET'),
        'authorize_url': 'https://www.tiktok.com/auth/authorize/',
        'token_url': 'https://open-api.tiktok.com/oauth/access_token/',
        'userinfo_url': 'https://open-api.tiktok.com/user/info/',
        'scope': 'user.info.basic',
        'platforms': ['TikTok']
    }
}

def get_oauth_config(platform):
    """Obtener configuración OAuth para una plataforma"""
    for provider, config in OAUTH_CONFIGS.items():
        if platform in config['platforms']:
            return provider, config
    return None, None
