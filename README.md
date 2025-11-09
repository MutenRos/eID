# eID - Meta Red Social

![eID Logo](https://via.placeholder.com/800x200/667eea/ffffff?text=eID+-+Tu+Identidad+Digital)

## 📋 Descripción

**eID** es una meta red social que funciona como tarjeta de visita digital. Permite a los usuarios centralizar todos sus perfiles de redes sociales en un único lugar, gestionar una agenda de contactos profesionales y comunicarse a través de un sistema de mensajería integrado.

Este proyecto es parte de la **Milla Extra del primer semestre** del ciclo **DAM (Desarrollo de Aplicaciones Multiplataforma)**.

## ✨ Características

- 🎴 **Perfil personalizable**: Bio, avatar, enlaces a redes sociales
- 🌐 **Agregación de RRSS**: Instagram, Twitter, LinkedIn, GitHub, etc.
- 👥 **Agenda de contactos**: Sistema de solicitudes y aceptación
- 💬 **Chat privado**: Mensajería entre contactos
- 🔐 **Autenticación segura**: Registro y login con contraseñas hasheadas
- 📱 **Diseño responsive**: Adaptado a móviles y tablets

## 🛠️ Tecnologías

- **Backend**: Python 3.12 + Flask
- **Base de datos**: SQLite + SQLAlchemy
- **Autenticación**: Flask-Login
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Control de versiones**: Git + GitHub

## 📂 Estructura del Proyecto

```
eID/
├── app/
│   ├── models/          # Modelos de datos (User, SocialLink, Contact, Message)
│   ├── routes/          # Rutas/controladores (auth, profile, contacts, chat)
│   ├── static/
│   │   ├── css/         # Estilos
│   │   ├── js/          # JavaScript
│   │   └── img/         # Imágenes
│   ├── templates/       # Plantillas HTML
│   └── __init__.py      # Factory de la aplicación
├── tests/               # Tests unitarios
├── docs/                # Documentación
├── run.py               # Punto de entrada
├── requirements.txt     # Dependencias
└── README.md
```

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- pip
- virtualenv (recomendado)

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/MutenRos/eID.git
cd eID
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar la aplicación**
```bash
python run.py
```

6. **Abrir en el navegador**
```
http://localhost:5000
```

## 📖 Uso

### Registro de usuario
1. Ir a `/auth/register`
2. Completar formulario con username, email y contraseña
3. Iniciar sesión en `/auth/login`

### Configurar perfil
1. Acceder a "Mi Perfil"
2. Editar información personal
3. Agregar enlaces a redes sociales

### Gestionar contactos
1. Buscar usuarios por nombre/username
2. Enviar solicitudes de contacto
3. Aceptar/rechazar solicitudes recibidas

### Chatear
1. Ir a la sección "Chat"
2. Seleccionar un contacto
3. Enviar mensajes

## 🗄️ Modelo de Datos

### User
- id, username, email, password_hash
- full_name, bio, avatar, website
- Relaciones: social_links, contacts, messages

### SocialLink
- platform (twitter, instagram, linkedin, github...)
- username, url, icon
- is_visible, order

### Contact
- user_id, contact_id
- status (pending, accepted, blocked)

### Message
- sender_id, receiver_id
- content, is_read, read_at

## 🔮 Roadmap

- [ ] Chat en tiempo real con WebSockets (Flask-SocketIO)
- [ ] Integración con APIs de RRSS para obtener datos automáticamente
- [ ] Temas personalizables para perfiles públicos
- [ ] Analíticas de visitas al perfil
- [ ] Exportación de tarjeta de visita en PDF
- [ ] Generación de códigos QR para compartir perfil
- [ ] Sistema de notificaciones
- [ ] Filtros y búsqueda avanzada de contactos

## 👨‍💻 Autor

**Darío Lacal Civera**
- GitHub: [@MutenRos](https://github.com/MutenRos)
- Proyecto: Milla Extra 1ª Evaluación DAM

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Profesores del ciclo DAM
- Comunidad de Flask y Python
- Todos los que contribuyan al proyecto

---

⭐ Si te gusta el proyecto, ¡dale una estrella en GitHub!