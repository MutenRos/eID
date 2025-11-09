# Instalación de eID con MySQL

## Requisitos Previos

- Python 3.8+
- MySQL 8.0+
- Git

## Pasos de Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MutenRos/eID.git
cd eID
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

#### Opción A: Desde MySQL Command Line

```bash
mysql -u root -p
```

```sql
SOURCE database_schema.sql;
```

#### Opción B: Desde MySQL Workbench

1. Abrir MySQL Workbench
2. Conectar a tu servidor local
3. File → Run SQL Script
4. Seleccionar `database_schema.sql`
5. Ejecutar

#### Opción C: Desde terminal (un solo comando)

```bash
mysql -u root -p < database_schema.sql
```

### 5. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Flask
SECRET_KEY=cambia-esto-por-algo-super-secreto-y-aleatorio
FLASK_ENV=development
FLASK_DEBUG=True

# MySQL
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=eid

# Aplicación
APP_NAME=eID
APP_VERSION=1.0.0
```

**Importante:** Cambia `DB_PASSWORD` por tu contraseña de MySQL.

### 6. Verificar conexión a la base de datos

```bash
python
```

```python
from app.database import db
db.connect()
# Si no hay errores, la conexión es exitosa
db.disconnect()
exit()
```

### 7. Ejecutar la aplicación

```bash
python run.py
```

### 8. Abrir en el navegador

```
http://localhost:5000
```

## Usuarios de Prueba

El script `database_schema.sql` incluye un usuario de prueba (comentado por defecto):

- **Usuario:** dario
- **Email:** dario@eid.com
- **Contraseña:** password123

Para activarlo, descomenta las líneas al final de `database_schema.sql` antes de ejecutarlo.

## Estructura de la Base de Datos

- **users**: Usuarios del sistema
- **social_links**: Enlaces a redes sociales de cada usuario
- **contacts**: Relaciones de contactos entre usuarios
- **messages**: Mensajes del chat

## Solución de Problemas

### Error: "Access denied for user 'root'@'localhost'"

- Verifica que tu contraseña de MySQL esté correcta en `.env`
- Asegúrate de que el servicio MySQL esté corriendo

### Error: "Unknown database 'eid'"

- Ejecuta el script `database_schema.sql` para crear la base de datos

### Error: "Table 'eid.users' doesn't exist"

- Vuelve a ejecutar `database_schema.sql`

### La aplicación no inicia

```bash
# Verificar que las dependencias están instaladas
pip list | grep Flask

# Reinstalar si es necesario
pip install -r requirements.txt --force-reinstall
```

## Comandos Útiles

### Ver tablas de la base de datos

```sql
USE eid;
SHOW TABLES;
DESCRIBE users;
```

### Limpiar base de datos

```sql
DROP DATABASE eid;
SOURCE database_schema.sql;
```

### Crear nuevo usuario desde MySQL

```sql
USE eid;
INSERT INTO users (username, email, password_hash, full_name) 
VALUES ('test', 'test@eid.com', 'scrypt:32768:8:1$...[hash]', 'Usuario de Prueba');
```

(Nota: Usa la aplicación web para crear usuarios, las contraseñas se hashean automáticamente)

## Desarrollo

### Ver logs de MySQL

```sql
SHOW VARIABLES LIKE 'general_log%';
SET GLOBAL general_log = 'ON';
```

### Backup de la base de datos

```bash
mysqldump -u root -p eid > backup_eid.sql
```

### Restaurar backup

```bash
mysql -u root -p eid < backup_eid.sql
```

## Próximos Pasos

1. Registrar un usuario en la aplicación
2. Completar tu perfil
3. Agregar tus redes sociales
4. Buscar y agregar contactos
5. Chatear con tus contactos

¡Listo! Ya tienes eID funcionando con MySQL.
