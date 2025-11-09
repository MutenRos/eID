# 🎯 Flujo de Usuario - Agregar Red Social

## Antes (Con campo username manual):
```
┌─────────────────────────────────────┐
│ 📘 Facebook                         │
├─────────────────────────────────────┤
│                                     │
│ Usuario de Facebook:                │
│ [tunombre________________]          │
│                                     │
│ URL de tu perfil:                   │
│ [https://facebook.com/tunombre___]  │
│                                     │
│ ☑ Mostrar en mi perfil             │
│                                     │
│ [💾 Guardar Facebook]               │
└─────────────────────────────────────┘
```

## Ahora (100% automático):
```
┌─────────────────────────────────────┐
│ 📘 Facebook                         │
├─────────────────────────────────────┤
│                                     │
│ URL de tu perfil *                  │
│ [https://facebook.com/dario.lacal_] │
│ Pega el enlace a tu perfil          │
│                                     │
│ ☑ Mostrar en mi perfil             │
│                                     │
│ [💾 Guardar Facebook]               │
└─────────────────────────────────────┘

         👇 Usuario hace clic

┌─────────────────────────────────────┐
│ ✅ Facebook actualizado              │
├─────────────────────────────────────┤
│ 📘 Facebook                         │
├─────────────────────────────────────┤
│ ╔═══════════════════════════════╗  │
│ ║ [AVATAR] Darío Lacal          ║  │
│ ║          dario.lacal          ║  │
│ ║                               ║  │
│ ║ Estudiante DAM | Desarrollador║  │
│ ║                               ║  │
│ ║ Ver perfil completo →         ║  │
│ ╚═══════════════════════════════╝  │
│                                     │
│ URL de tu perfil *                  │
│ [https://facebook.com/dario.lacal_] │
│                                     │
│ ☑ Mostrar en mi perfil             │
│                                     │
│ [💾 Actualizar Facebook]            │
└─────────────────────────────────────┘
```

## 🔄 Lo que hace el sistema automáticamente:

1. **Extrae username de la URL:**
   ```
   https://facebook.com/dario.lacal
                        ↓
                   dario.lacal
   ```

2. **Hace scraping de la página:**
   ```html
   <meta property="og:title" content="Darío Lacal">
   <meta property="og:description" content="Estudiante DAM | Desarrollador">
   <meta property="og:image" content="https://...avatar.jpg">
   ```

3. **Guarda la información:**
   ```json
   {
     "username": "dario.lacal",
     "profile_name": "Darío Lacal",
     "avatar": "https://...avatar.jpg",
     "bio": "Estudiante DAM | Desarrollador"
   }
   ```

4. **Muestra preview bonito:**
   - Avatar (si existe)
   - Nombre completo
   - Username
   - Biografía
   - Enlace al perfil

## 📱 Ejemplo para cada plataforma:

### WhatsApp
```
Usuario pega: https://wa.me/34600123456
Sistema extrae: +34 600 123 456
```

### Instagram
```
Usuario pega: https://instagram.com/rosfehn
Sistema extrae: @rosfehn + foto + bio
```

### LinkedIn
```
Usuario pega: https://linkedin.com/in/dario-lacal
Sistema extrae: dario-lacal + nombre + puesto
```

### YouTube
```
Usuario pega: https://youtube.com/@MiCanal
Sistema extrae: @MiCanal + nombre del canal + avatar
```

## ✨ Ventajas del nuevo flujo:

✅ **Más rápido:** Solo pega la URL y listo
✅ **Sin errores:** No hay que escribir el username
✅ **Información rica:** Muestra avatar, bio, etc.
✅ **Visual:** Preview inmediato del perfil
✅ **Actualizable:** Volver a guardar actualiza la info

## 🎯 Resultado final:

**Usuario solo necesita:**
1. Ir a su red social
2. Copiar la URL de su perfil
3. Pegarla en eID
4. Click en "Guardar"

**eID se encarga de:**
- Extraer el username
- Obtener la foto
- Leer la bio
- Formatear todo bonito
- Mostrarlo en el perfil

**¡100% automático! 🚀**
