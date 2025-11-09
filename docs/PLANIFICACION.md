# eID - Planificación del Proyecto
**Milla Extra 1ª Evaluación DAM**

## 📋 Información del Proyecto

**Nombre:** eID (Electronic Identity)  
**Tipo:** Meta red social / Tarjeta de visita digital  
**Autor:** Darío Lacal Civera  
**Fecha inicio:** 9 de noviembre de 2025  
**Repositorio:** https://github.com/MutenRos/eID

## 🎯 Objetivos del Proyecto

### Objetivo Principal
Crear una plataforma web que centralice la identidad digital de los usuarios, permitiendo:
- Agregar enlaces a todas sus redes sociales
- Gestionar una agenda de contactos profesionales
- Comunicarse mediante un sistema de chat integrado

### Objetivos Secundarios
1. Aplicar conocimientos de **Programación** (Python, POO)
2. Integrar **Bases de Datos** (SQLAlchemy, modelos relacionales)
3. Utilizar **Lenguajes de Marcas** (HTML5, CSS3)
4. Implementar **Sistemas Informáticos** (despliegue, servidor web)
5. Practicar **Entornos de Desarrollo** (Git, GitHub, debugging)

## 🗓️ Cronograma

### Fase 1: Infraestructura (Semana 1) ✅
- [x] Crear repositorio en GitHub
- [x] Configurar estructura del proyecto Flask
- [x] Definir modelos de datos (User, SocialLink, Contact, Message)
- [x] Implementar sistema de autenticación
- [x] Crear templates base y estilos

### Fase 2: Funcionalidades Core (Semana 2)
- [ ] Sistema de perfiles de usuario
  - [ ] Visualización de perfil público
  - [ ] Edición de perfil
  - [ ] Upload de avatar
- [ ] Gestión de enlaces sociales
  - [ ] Agregar/eliminar redes sociales
  - [ ] Ordenar enlaces por drag & drop
  - [ ] Toggle de visibilidad

### Fase 3: Red Social (Semana 3)
- [ ] Agenda de contactos
  - [ ] Búsqueda de usuarios
  - [ ] Envío de solicitudes
  - [ ] Aceptar/rechazar contactos
  - [ ] Listado de contactos
- [ ] Sistema de mensajería
  - [ ] Chat 1 a 1
  - [ ] Historial de mensajes
  - [ ] Indicadores de leído/no leído

### Fase 4: Mejoras y Pulido (Semana 4)
- [ ] Responsive design (mobile-first)
- [ ] Validaciones de formularios
- [ ] Mensajes flash mejorados
- [ ] Paginación de mensajes
- [ ] Testing básico

### Fase 5: Extras Opcionales
- [ ] Chat en tiempo real (WebSockets)
- [ ] Integración con APIs de RRSS
- [ ] Temas personalizables
- [ ] Generación de QR para perfil
- [ ] Exportación de tarjeta en PDF
- [ ] Analíticas de visitas

## 📊 Arquitectura del Sistema

### Stack Tecnológico

**Backend:**
- Python 3.12
- Flask 3.0
- SQLAlchemy 2.0
- Flask-Login (autenticación)
- Werkzeug (seguridad)

**Frontend:**
- HTML5
- CSS3 (Grid, Flexbox, Variables CSS)
- JavaScript vanilla (sin frameworks)

**Base de Datos:**
- SQLite (desarrollo)
- Posible migración a PostgreSQL (producción)

**Control de Versiones:**
- Git
- GitHub

### Estructura de Directorios

```
eID/
├── app/
│   ├── models/              # Capa de datos
│   │   ├── user.py
│   │   ├── social_link.py
│   │   ├── contact.py
│   │   └── message.py
│   ├── routes/              # Capa de lógica
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── contacts.py
│   │   └── chat.py
│   ├── static/              # Recursos estáticos
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   ├── templates/           # Vistas
│   └── __init__.py          # Factory
├── tests/                   # Testing
├── docs/                    # Documentación
├── run.py                   # Entry point
├── requirements.txt
└── .gitignore
```

## 🗄️ Modelo de Datos

### Entidades

#### User
```python
- id: Integer (PK)
- username: String (unique)
- email: String (unique)
- password_hash: String
- full_name: String
- bio: Text
- avatar: String
- website: String
- created_at: DateTime
- is_active: Boolean
```

#### SocialLink
```python
- id: Integer (PK)
- user_id: Integer (FK -> User)
- platform: String (twitter, instagram, linkedin...)
- username: String
- url: String
- icon: String
- is_visible: Boolean
- order: Integer
```

#### Contact
```python
- id: Integer (PK)
- user_id: Integer (FK -> User)
- contact_id: Integer (FK -> User)
- status: String (pending, accepted, blocked)
- created_at: DateTime
- accepted_at: DateTime
```

#### Message
```python
- id: Integer (PK)
- sender_id: Integer (FK -> User)
- receiver_id: Integer (FK -> User)
- content: Text
- is_read: Boolean
- read_at: DateTime
- created_at: DateTime
```

### Relaciones

- User → SocialLink: 1:N
- User → Contact: N:N (self-referencing)
- User → Message: 1:N (como sender y receiver)

## 🎨 Diseño UI/UX

### Paleta de Colores
```css
Primary: #667eea (Azul/Morado)
Secondary: #764ba2 (Morado oscuro)
Success: #2ecc71 (Verde)
Danger: #e74c3c (Rojo)
Dark: #2c3e50
Light: #ecf0f1
```

### Páginas Principales

1. **Landing Page** (/)
   - Hero section con CTA
   - Características del servicio
   - Registro/Login

2. **Dashboard** (/profile/me)
   - Resumen del perfil
   - Enlaces rápidos a funcionalidades
   - Estadísticas básicas

3. **Perfil Público** (/profile/:username)
   - Información del usuario
   - Redes sociales visibles
   - Botón de contacto

4. **Contactos** (/contacts)
   - Buscador de usuarios
   - Solicitudes pendientes
   - Lista de contactos

5. **Chat** (/chat)
   - Lista de conversaciones
   - Chat individual
   - Indicadores de actividad

## 🔐 Seguridad

### Implementadas
- ✅ Contraseñas hasheadas (Werkzeug)
- ✅ Flask-Login para sesiones
- ✅ CSRF protection (Flask-WTF)
- ✅ Validación de permisos en rutas

### Por implementar
- [ ] Rate limiting (Flask-Limiter)
- [ ] Validación de inputs (WTForms)
- [ ] HTTPS en producción
- [ ] Sanitización de contenido HTML

## 📈 Métricas de Éxito

### Funcionalidad
- [ ] Usuario puede registrarse y hacer login
- [ ] Usuario puede editar su perfil
- [ ] Usuario puede agregar 5+ redes sociales
- [ ] Usuario puede buscar y agregar contactos
- [ ] Usuario puede enviar/recibir mensajes

### Calidad de Código
- [ ] Sin errores de lint
- [ ] Modelos bien estructurados
- [ ] Código documentado
- [ ] Git commits descriptivos

### UX
- [ ] Diseño responsive
- [ ] Tiempos de carga < 2s
- [ ] Navegación intuitiva
- [ ] Feedback visual de acciones

## 🚀 Despliegue

### Desarrollo
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### Producción (Futura)
- Plataforma: Railway / Render / PythonAnywhere
- Base de datos: PostgreSQL
- Servidor: Gunicorn
- Proxy: Nginx

## 📚 Recursos de Aprendizaje

### Documentación
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Flask-Login](https://flask-login.readthedocs.io/)

### Tutoriales
- Miguel Grinberg's Flask Mega-Tutorial
- Real Python - Flask tutorials
- Corey Schafer - Flask series

## 🐛 Issues y Mejoras

### Issues Conocidos
- [ ] Falta paginación en listado de mensajes
- [ ] No hay validación de formato de URLs
- [ ] Avatar solo soporta imágenes por defecto

### Mejoras Futuras
- [ ] Notificaciones en tiempo real
- [ ] Modo oscuro
- [ ] Exportar perfil como vCard
- [ ] Integración con redes sociales (OAuth)
- [ ] API REST para mobile app

## 📝 Notas de Desarrollo

### Decisiones Técnicas

**¿Por qué Flask y no Django?**
- Mayor control sobre la estructura
- Curva de aprendizaje más suave
- Mejor para proyectos pequeños/medianos
- Más ligero y flexible

**¿Por qué SQLite?**
- No requiere servidor separado
- Perfecto para desarrollo
- Migración sencilla a PostgreSQL

**¿Por qué JavaScript vanilla?**
- Evitar complejidad innecesaria
- Aprender fundamentos antes de frameworks
- Mejor rendimiento para funcionalidades simples

### Lecciones Aprendidas
- (Se irán documentando durante el desarrollo)

---

**Última actualización:** 9 de noviembre de 2025
