# 🔗 Extractor de Información de Redes Sociales - eID

## ✨ Funcionalidad

Cuando un usuario pega el enlace a su perfil de una red social, **eID automáticamente extrae y muestra**:

- ✅ Nombre de usuario/handle
- ✅ Nombre del perfil
- ✅ Avatar/foto de perfil
- ✅ Biografía
- ✅ Número de seguidores (cuando está disponible)
- ✅ Estado de verificación

## 🚀 ¿Cómo funciona?

### 1. **Parseo de URL**
Extrae el username directamente de la estructura de la URL:
- Instagram: `instagram.com/username` → `@username`
- Twitter/X: `x.com/username` → `@username`
- Facebook: `facebook.com/username` → `username`
- LinkedIn: `linkedin.com/in/username` → `username`
- YouTube: `youtube.com/@channel` → `@channel`
- TikTok: `tiktok.com/@username` → `@username`
- WhatsApp: `wa.me/34600000000` → `+34 600 000 000`

### 2. **Web Scraping Básico**
Intenta obtener metadata de la página usando:
- **Open Graph tags** (`og:title`, `og:description`, `og:image`)
- **Meta tags** estándar
- **Título de la página**

### 3. **Sin APIs ni OAuth**
- ❌ No requiere tokens de API
- ❌ No necesita permisos OAuth
- ❌ No hay límites de rate limiting
- ✅ Funciona con enlaces públicos
- ✅ No requiere credenciales de terceros

## 📋 Ejemplo de Uso

**Usuario pega:**
```
https://instagram.com/rosfehn
```

**eID extrae automáticamente:**
- Username: `@rosfehn`
- Nombre del perfil: (del meta tag `og:title`)
- Avatar: (de `og:image`)
- Bio: (de `og:description`)

**Y muestra un preview visual:**
```
┌─────────────────────────────────┐
│  [AVATAR]  Nombre del Perfil    │
│            @rosfehn             │
│                                 │
│  Texto de la biografía...       │
│                                 │
│  Ver perfil completo →          │
└─────────────────────────────────┘
```

## ⚙️ Arquitectura

### Archivos modificados/creados:

1. **`app/social_extractor.py`**
   - Función `extract_social_info(url, platform)` - Extractor principal
   - Parsers específicos por plataforma
   - Scraper básico con BeautifulSoup

2. **`app/routes/profile.py`**
   - Actualizado `save_social_link()` para llamar al extractor
   - Guarda `profile_data` como JSON en la BD

3. **`app/templates/profile/view.html`**
   - Muestra preview visual de la información extraída
   - Estilos CSS para `.social-preview`

4. **`requirements.txt`**
   - Añadido: `beautifulsoup4==4.12.2`

## 🎨 Vista del Usuario

### Antes de guardar:
```
URL de tu perfil: [https://facebook.com/tunombre    ]
                  [Guardar Facebook]
```

### Después de guardar:
```
╔═══════════════════════════════════╗
║  [📘]  Tu Nombre                  ║
║         tunombre                  ║
║                                   ║
║  Esta es tu biografía de Facebook ║
║                                   ║
║  Ver perfil completo →            ║
╚═══════════════════════════════════╝

URL de tu perfil: [https://facebook.com/tunombre    ]
                  [Actualizar Facebook]
```

## 🔒 Limitaciones

### Lo que SÍ funciona:
- ✅ Perfiles públicos de todas las plataformas
- ✅ Extracción de username de la URL
- ✅ Meta tags Open Graph (si existen)
- ✅ URLs formateadas correctamente

### Lo que NO funciona:
- ❌ Perfiles privados (no hay acceso)
- ❌ Plataformas que bloquean scraping (Instagram, Facebook protegido)
- ❌ Contenido que requiere JavaScript (single-page apps)
- ❌ Información de métricas en tiempo real (seguidores, likes)

### Fallback:
Si el scraping falla, **siempre se guarda**:
- ✅ La URL proporcionada
- ✅ El username extraído de la URL
- ⚠️ Mensaje: "No se pudo obtener información adicional"

## 💡 Ventajas del MVP

1. **Simplicidad**: No requiere configuración de APIs
2. **Sin costes**: No hay límites de API que pagar
3. **Privacidad**: No se almacenan tokens de terceros
4. **Rapidez**: No hay flujos OAuth complicados
5. **Funciona offline**: Solo necesita la URL

## 🚀 Próximas Mejoras (Opcionales)

- [ ] Cache de información extraída
- [ ] Actualización automática periódica
- [ ] Validación de URLs antes de guardar
- [ ] Soporte para más plataformas (GitHub, Twitch, etc.)
- [ ] Vista previa en tiempo real (AJAX)

---

**Resultado:** Usuario pega un enlace → Sistema extrae info → Muestra preview bonito ✨
