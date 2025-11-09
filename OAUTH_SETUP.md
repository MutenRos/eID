# Guía de Configuración OAuth - eID

Esta guía te ayudará a configurar la integración OAuth con cada red social para que los usuarios puedan conectar sus cuentas con un solo clic.

## 📋 Requisitos Previos

1. Tener el servidor eID corriendo en un dominio público o usar **ngrok** para desarrollo
2. Instalar la dependencia: `pip install requests`

## 🔧 Configuración por Plataforma

### 1. 📺 YouTube (Google OAuth)

**Paso 1:** Ir a [Google Cloud Console](https://console.cloud.google.com/)

**Paso 2:** Crear un nuevo proyecto o seleccionar uno existente

**Paso 3:** Habilitar APIs:
- YouTube Data API v3
- Google+ API (para perfil)

**Paso 4:** Crear credenciales OAuth 2.0:
- Ir a "Credenciales" → "Crear credenciales" → "ID de cliente de OAuth 2.0"
- Tipo de aplicación: **Aplicación web**
- URIs de redireccionamiento autorizados:
  - `http://localhost:5000/oauth/callback/YouTube` (desarrollo)
  - `https://tudominio.com/oauth/callback/YouTube` (producción)

**Paso 5:** Copiar Client ID y Client Secret al archivo `.env`:
```bash
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-client-secret
```

---

### 2. 📘 Facebook + 📷 Instagram

**Paso 1:** Ir a [Meta for Developers](https://developers.facebook.com/)

**Paso 2:** Crear una nueva aplicación:
- Tipo: **Consumer** (para usuarios finales)

**Paso 3:** Agregar productos:
- **Facebook Login**
- **Instagram Basic Display** (para Instagram)

**Paso 4:** Configurar Facebook Login:
- URIs de redireccionamiento válidos:
  - `http://localhost:5000/oauth/callback/Facebook`
  - `https://tudominio.com/oauth/callback/Facebook`

**Paso 5:** Configurar Instagram Basic Display:
- URIs de redireccionamiento:
  - `http://localhost:5000/oauth/callback/Instagram`
  - `https://tudominio.com/oauth/callback/Instagram`
- Agregar usuarios de prueba (Instagram)

**Paso 6:** Copiar credenciales al `.env`:
```bash
FACEBOOK_APP_ID=tu-app-id
FACEBOOK_APP_SECRET=tu-app-secret
```

**Nota:** Para Instagram, necesitas aprobar la app en Meta antes de que funcione para todos los usuarios.

---

### 3. ✖️ X (Twitter)

**Paso 1:** Ir a [Twitter Developer Portal](https://developer.twitter.com/en/portal)

**Paso 2:** Crear un nuevo proyecto y aplicación

**Paso 3:** En "User authentication settings":
- Tipo: **Web App, Automated App or Bot**
- Permisos: **Read** (solo lectura)
- Callback URL:
  - `http://localhost:5000/oauth/callback/X`
  - `https://tudominio.com/oauth/callback/X`
- Website URL: Tu dominio

**Paso 4:** Guardar Client ID y Client Secret:
```bash
TWITTER_CLIENT_ID=tu-client-id
TWITTER_CLIENT_SECRET=tu-client-secret
```

---

### 4. 💼 LinkedIn

**Paso 1:** Ir a [LinkedIn Developers](https://www.linkedin.com/developers/)

**Paso 2:** Crear una nueva aplicación

**Paso 3:** Configurar OAuth 2.0:
- Redirect URLs:
  - `http://localhost:5000/oauth/callback/LinkedIn`
  - `https://tudominio.com/oauth/callback/LinkedIn`

**Paso 4:** Solicitar permisos (Products):
- **Sign In with LinkedIn**

**Paso 5:** Copiar credenciales:
```bash
LINKEDIN_CLIENT_ID=tu-client-id
LINKEDIN_CLIENT_SECRET=tu-client-secret
```

---

### 5. 🎵 TikTok

**Paso 1:** Ir a [TikTok for Developers](https://developers.tiktok.com/)

**Paso 2:** Crear una nueva aplicación

**Paso 3:** Configurar:
- Redirect URI:
  - `http://localhost:5000/oauth/callback/TikTok`
  - `https://tudominio.com/oauth/callback/TikTok`

**Paso 4:** Solicitar permisos:
- `user.info.basic`

**Paso 5:** Guardar credenciales:
```bash
TIKTOK_CLIENT_KEY=tu-client-key
TIKTOK_CLIENT_SECRET=tu-client-secret
```

---

## 🚀 Desarrollo Local con ngrok

Si estás desarrollando localmente, las plataformas requieren HTTPS. Usa **ngrok**:

```bash
# Instalar ngrok
winget install ngrok

# Iniciar túnel
ngrok http 5000
```

Esto te dará una URL como `https://abc123.ngrok.io`. Úsala en las configuraciones OAuth.

---

## 📝 Archivo .env Completo

```bash
# Flask
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
FLASK_ENV=development
FLASK_DEBUG=True

# Base de datos MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=eid

# OAuth - Google (YouTube)
GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abc123def456
# OAuth - Facebook (Facebook + Instagram)
FACEBOOK_APP_ID=123456789012345
FACEBOOK_APP_SECRET=abc123def456ghi789

# OAuth - Twitter/X
TWITTER_CLIENT_ID=abc123def456
TWITTER_CLIENT_SECRET=xyz789uvw012

# OAuth - LinkedIn
LINKEDIN_CLIENT_ID=abc123def456
LINKEDIN_CLIENT_SECRET=xyz789uvw012

# OAuth - TikTok
TIKTOK_CLIENT_KEY=abc123def456
TIKTOK_CLIENT_SECRET=xyz789uvw012
```

---

## ✅ Verificación

Una vez configurado todo:

1. Reinicia el servidor Flask
2. Ve a **Mi Perfil** → Pestaña de la red social
3. Haz clic en **"🔗 Conectar con [Plataforma]"**
4. Autoriza en la ventana emergente
5. Serás redirigido de vuelta y tu perfil se conectará automáticamente

---

## ⚠️ Notas Importantes

- **WhatsApp:** No tiene OAuth oficial. Se mantiene entrada manual.
- **Instagram:** Requiere aprobación de Meta para usuarios no-testers.
- **Modo desarrollo:** Las apps en modo desarrollo solo funcionan para usuarios autorizados.
- **HTTPS requerido:** Para producción, necesitas un dominio con SSL.
- **Rate limits:** Cada plataforma tiene límites de peticiones. No abuses.

---

## 🔒 Seguridad

- **NUNCA** subas el archivo `.env` a GitHub
- Usa variables de entorno en producción
- Revoca tokens si sospechas compromiso
- Implementa rate limiting en las rutas OAuth
