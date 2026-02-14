# eID — Meta Red Social · Tarjeta de Visita Digital

![eID hero](app/templates/index.html)

---

## Introducción

![Pantalla de login con Google OAuth](app/templates/auth/login.html)

**eID** es una meta red social que funciona como tarjeta de visita digital. Permite a cada usuario centralizar todos sus perfiles de redes sociales (Instagram, Twitter, LinkedIn, GitHub…) en un único lugar, gestionar una agenda de contactos profesionales mediante códigos de amigo, comunicarse con chat privado y organizar eventos en un calendario compartido.

El proyecto está construido con **Python/Flask** como backend, **MySQL** como base de datos relacional (5 tablas con claves foráneas), plantillas **Jinja2** para el frontend, **CSS** responsive con variables custom y **JavaScript** vanilla para chat en tiempo real y drag-and-drop de carpetas. También integra **Google OAuth 2.0** para registro/login con un clic.

---

## Desarrollo de las partes

### 1. Modelo de datos — Esquema relacional MySQL

El esquema relacional consta de 5 tablas principales: `users` (perfil, friend_code, OAuth), `social_links` (redes sociales con FK a users), `contacts` (solicitudes con ENUM pending/accepted/blocked), `messages` (chat con is_read y read_at) y `calendar_events` (eventos con participantes). Todas usan motor InnoDB con integridad referencial y encoding UTF-8mb4.

**Código relevante:**

- Tabla `users` con índices en username, email y friend_code para búsquedas rápidas:
  - **Archivo:** `database_schema.sql` · **Líneas 8-25** · **Ruta:** `database_schema.sql`
- Tabla `contacts` con ENUM para estados y UNIQUE KEY para evitar duplicados:
  - **Archivo:** `database_schema.sql` · **Líneas 44-60** · **Ruta:** `database_schema.sql`
- Tabla `messages` con índices en sender, receiver y created_at para ordenar conversaciones:
  - **Archivo:** `database_schema.sql` · **Líneas 63-79** · **Ruta:** `database_schema.sql`
- Vista `user_stats` que agrega contactos, mensajes y redes de cada usuario con subconsultas:
  - **Archivo:** `database_schema.sql` · **Líneas 87-100** · **Ruta:** `database_schema.sql`

---

### 2. Capa de acceso a datos — `database.py`

Clase `Database` que encapsula la conexión a MySQL con métodos `execute_query()` (INSERT/UPDATE/DELETE con commit y rollback), `fetch_one()` y `fetch_all()` (SELECT con cursor dictionary). Usa variables de entorno para host/port/user/password, charset UTF-8mb4 y cierre automático en cada request de Flask.

**Código relevante:**

- Constructor con variables de entorno y valores por defecto:
  - **Archivo:** `database.py` · **Líneas 9-19** · **Ruta:** `app/database.py`
- Método `connect()` con charset utf8mb4 y collation:
  - **Archivo:** `database.py` · **Líneas 21-35** · **Ruta:** `app/database.py`
- Método `execute_query()` con try/except, commit y rollback ante errores:
  - **Archivo:** `database.py` · **Líneas 44-58** · **Ruta:** `app/database.py`
- Método `fetch_one()` con cursor dictionary para devolver diccionarios en vez de tuplas:
  - **Archivo:** `database.py` · **Líneas 60-73** · **Ruta:** `app/database.py`

---

### 3. Modelo de Usuario — `user.py` con Flask-Login

Modelo `User` que extiende `UserMixin` de Flask-Login. Incluye creación de usuarios con contraseña hasheada (`generate_password_hash`), generación de `friend_code` único de 8 caracteres (letras + dígitos), búsqueda por username/email/friend_code/google_id, y vinculación de cuentas con Google OAuth.

**Código relevante:**

- Generación de código de amigo único con `secrets.choice()`:
  - **Archivo:** `user.py` · **Líneas 35-43** · **Ruta:** `app/models/user.py`
- Creación de usuario con password hasheado (Werkzeug `generate_password_hash`):
  - **Archivo:** `user.py` · **Líneas 45-55** · **Ruta:** `app/models/user.py`
- Búsqueda por friend_code con consulta parametrizada:
  - **Archivo:** `user.py` · **Líneas 106-111** · **Ruta:** `app/models/user.py`
- Método `check_password()` que verifica hash y gestiona usuarios OAuth sin contraseña:
  - **Archivo:** `user.py` · **Líneas 125-129** · **Ruta:** `app/models/user.py`
- Carga de usuario para Flask-Login decorada con `@login_manager.user_loader`:
  - **Archivo:** `user.py` · **Líneas 160-163** · **Ruta:** `app/models/user.py`

---

### 4. Modelo de Contactos — Sistema de solicitudes

Modelo `Contact` con métodos estáticos que manejan todo el flujo de contactos: `create()` genera solicitudes pending, `exists()` verifica relaciones bidireccionales, `get_accepted()` usa un CASE WHEN + JOIN para obtener el contacto correcto desde ambos lados de la relación, y `are_contacts()` valida si dos usuarios son contactos mutuos aceptados.

**Código relevante:**

- Verificación bidireccional de contacto existente con OR en WHERE:
  - **Archivo:** `contact.py` · **Líneas 18-24** · **Ruta:** `app/models/contact.py`
- JOIN con CASE WHEN para resolver el lado correcto del contacto:
  - **Archivo:** `contact.py` · **Líneas 27-42** · **Ruta:** `app/models/contact.py`
- Aceptar solicitud actualizando status y `accepted_at`:
  - **Archivo:** `contact.py` · **Líneas 70-76** · **Ruta:** `app/models/contact.py`

---

### 5. Chat privado — Mensajería en tiempo real

El modelo `Message` gestiona la conversación entre usuarios con `create()`, `get_conversation()` (ORDER BY created_at ASC), `mark_as_read()` (actualiza is_read y read_at) y `count_unread()`. La ruta `/chat/<user_id>` verifica que los usuarios sean contactos antes de mostrar mensajes. El JS los actualiza cada 5 segundos con `fetch('/chat/unread-count')`.

**Código relevante:**

- Obtención de conversación bidireccional con OR y ORDER ASC:
  - **Archivo:** `message.py` · **Líneas 18-25** · **Ruta:** `app/models/message.py`
- Marcar mensajes como leídos con CURRENT_TIMESTAMP:
  - **Archivo:** `message.py` · **Líneas 28-34** · **Ruta:** `app/models/message.py`
- Ruta de conversación que verifica contacto mutuo antes de mostrar chat:
  - **Archivo:** `chat.py` · **Líneas 25-43** · **Ruta:** `app/routes/chat.py`
- Validación de mensaje: strip, longitud > 0 y límite de 2000 caracteres:
  - **Archivo:** `chat.py` · **Líneas 51-60** · **Ruta:** `app/routes/chat.py`
- Polling JS cada 5 segundos para actualizar badge de no leídos:
  - **Archivo:** `main.js` · **Líneas 3-17** · **Ruta:** `app/static/js/main.js`

---

### 6. Autenticación — Registro, login y Google OAuth

El blueprint `auth` implementa registro con validaciones (mínimo 6 caracteres, regex de username), login por username o email, y flujo completo de OAuth 2.0 con Google (autorización → callback → intercambio de token → userinfo → creación o vinculación de cuenta). Usa `secrets.token_urlsafe(32)` como state anti-CSRF.

**Código relevante:**

- Validación de contraseña mínima y regex de username en registro:
  - **Archivo:** `auth.py` · **Líneas 22-35** · **Ruta:** `app/routes/auth.py`
- Login flexible que busca por username o email:
  - **Archivo:** `auth.py` · **Líneas 56-59** · **Ruta:** `app/routes/auth.py`
- Generación de state anti-CSRF para OAuth:
  - **Archivo:** `auth.py` · **Líneas 96-97** · **Ruta:** `app/routes/auth.py`
- Callback de Google: intercambio de código por token de acceso:
  - **Archivo:** `auth.py` · **Líneas 142-157** · **Ruta:** `app/routes/auth.py`
- Vinculación de cuenta existente con cuenta Google:
  - **Archivo:** `auth.py` · **Líneas 186-200** · **Ruta:** `app/routes/auth.py`

---

### 7. Factory de la aplicación y blueprints — `__init__.py`

La función `create_app()` sigue el patrón Factory de Flask: configura SECRET_KEY desde variable de entorno, inicializa Flask-Login, conecta la BD antes de cada request con `@before_request`, la desconecta con `@teardown_request` y registra 7 blueprints (main, auth, profile, contacts, chat, oauth, calendar).

**Código relevante:**

- Inicialización de Flask-Login con vista de login por defecto:
  - **Archivo:** `__init__.py` · **Líneas 23-24** · **Ruta:** `app/__init__.py`
- Hook `before_request` para reconectar a la BD si la conexión se perdió:
  - **Archivo:** `__init__.py` · **Líneas 28-30** · **Ruta:** `app/__init__.py`
- Registro de los 7 blueprints modulares:
  - **Archivo:** `__init__.py` · **Líneas 38-45** · **Ruta:** `app/__init__.py`

---

### 8. Frontend — Templates Jinja2, CSS y JavaScript

El frontend usa un `base.html` con navbar dinámica (autenticado vs anónimo), sistema de alertas flash con categorías, y un footer. El CSS define variables custom (--primary, --secondary) con gradientes, grid responsive y backdrop-filter. El JS gestiona polling de mensajes no leídos, auto-cierre de alertas, contador de caracteres y copia al portapapeles.

**Código relevante:**

- Navbar condicional con badge de mensajes no leídos:
  - **Archivo:** `base.html` · **Líneas 17-29** · **Ruta:** `app/templates/base.html`
- Variables CSS custom y gradiente hero:
  - **Archivo:** `style.css` · **Líneas 3-15** · **Ruta:** `app/static/css/style.css`
- Grid responsive con `auto-fit` + `minmax` para features del hero:
  - **Archivo:** `style.css` · **Líneas 103-106** · **Ruta:** `app/static/css/style.css`
- Indicador de fuerza de contraseña en registro:
  - **Archivo:** `register.html` · **Líneas 55-65** · **Ruta:** `app/templates/auth/register.html`
- Contador de caracteres del chat con clases warning/danger:
  - **Archivo:** `main.js` · **Líneas 78-92** · **Ruta:** `app/static/js/main.js`

---

## Presentación del proyecto

eID es una aplicación web que actúa como tarjeta de visita digital: al crear tu cuenta recibes un código de amigo de 8 caracteres que puedes compartir para que otros usuarios te agreguen a su agenda. Una vez conectados, podéis ver mutuamente vuestros perfiles con todas las redes sociales enlazadas, chatear en tiempo real y compartir eventos de calendario.

Al acceder a eID se muestra la landing page con tres features principales: Meta Red Social, Agenda de Contactos y Chat Integrado. Desde ahí el usuario puede registrarse con email y contraseña o con Google OAuth en un clic. El indicador de fuerza de contraseña guía al usuario durante el registro.

Una vez dentro, la sección "Mi Perfil" muestra la bio, el avatar y los enlaces a redes sociales del usuario. La pestaña de contactos muestra el código de amigo propio con botón de copiar, un campo para agregar contactos por código, solicitudes pendientes y la lista de contactos aceptados organizados en carpetas con drag-and-drop.

El chat permite mantener conversaciones privadas entre contactos con mensajes en burbujas (azul para enviados, blanco para recibidos), indicador de lectura (✓✓), polling automático de mensajes no leídos cada 5 segundos y badge numérico en la navbar. El calendario permite crear eventos con color, tipo, ubicación, recordatorios y asignar contactos como participantes.

Todo el backend usa consultas parametrizadas con `%s` para prevenir inyección SQL, contraseñas hasheadas con scrypt, validaciones de entrada, y sesiones seguras con Flask-Login.

---

## Conclusión

eID demuestra la construcción de una aplicación web completa que integra las capas fundamentales de un proyecto de bases de datos: un esquema relacional normalizado en MySQL con 5 tablas e integridad referencial, una capa de acceso a datos en Python con gestión de conexiones y transacciones, lógica de negocio con Flask organizada en 7 blueprints, autenticación segura con hashing y OAuth 2.0, y un frontend responsive con JavaScript vanilla.

Las claves del proyecto son:

- **Base de datos:** 5 tablas con FKs, ENUMs, índices optimizados, vista agregada y motor InnoDB
- **Seguridad:** contraseñas hasheadas (scrypt), consultas parametrizadas anti-SQLi, state anti-CSRF en OAuth, validación de inputs, verificación de permisos entre contactos
- **Arquitectura:** patrón Factory de Flask, blueprints modulares, modelos con métodos estáticos, capa de base de datos centralizada
- **UX:** código de amigo único, Google OAuth, chat con polling, drag-and-drop de carpetas, calendario compartido

El resultado es una red social funcional que va más allá de un CRUD básico: implementa relaciones bidireccionales, mensajería en tiempo real, OAuth con vincualción de cuentas y un sistema de eventos con participantes, todo manteniendo una arquitectura limpia y mantenible.
