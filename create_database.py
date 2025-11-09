"""Script para crear la base de datos eID en MySQL"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_database():
    """Crear base de datos y tablas"""
    try:
        # Conectar sin especificar base de datos
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '3306'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '')
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Crear base de datos
            print("Creando base de datos 'eid'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS eid CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute("USE eid")
            print("✓ Base de datos 'eid' creada")
            
            # Crear tabla users
            print("\nCreando tabla 'users'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) NOT NULL UNIQUE,
                    email VARCHAR(120) NOT NULL UNIQUE,
                    password_hash VARCHAR(200) NOT NULL,
                    full_name VARCHAR(100),
                    bio TEXT,
                    avatar VARCHAR(200) DEFAULT 'default.png',
                    website VARCHAR(200),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    INDEX idx_username (username),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB
            """)
            print("✓ Tabla 'users' creada")
            
            # Crear tabla social_links
            print("Creando tabla 'social_links'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS social_links (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    platform VARCHAR(50) NOT NULL,
                    username VARCHAR(100) NOT NULL,
                    url VARCHAR(500) NOT NULL,
                    icon VARCHAR(50),
                    is_visible BOOLEAN DEFAULT TRUE,
                    display_order INT DEFAULT 0,
                    profile_data JSON,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id)
                ) ENGINE=InnoDB
            """)
            print("✓ Tabla 'social_links' creada")
            
            # Crear tabla contacts
            print("Creando tabla 'contacts'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contacts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    contact_id INT NOT NULL,
                    status ENUM('pending', 'accepted', 'blocked') DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    accepted_at TIMESTAMP NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (contact_id) REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_contact (user_id, contact_id),
                    INDEX idx_user_id (user_id),
                    INDEX idx_contact_id (contact_id),
                    INDEX idx_status (status)
                ) ENGINE=InnoDB
            """)
            print("✓ Tabla 'contacts' creada")
            
            # Crear tabla messages
            print("Creando tabla 'messages'...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sender_id INT NOT NULL,
                    receiver_id INT NOT NULL,
                    content TEXT NOT NULL,
                    is_read BOOLEAN DEFAULT FALSE,
                    read_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_sender (sender_id),
                    INDEX idx_receiver (receiver_id),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB
            """)
            print("✓ Tabla 'messages' creada")
            
            connection.commit()
            print("\n✅ Base de datos 'eid' creada exitosamente con todas las tablas!")
            
            # Mostrar estadísticas
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\nTablas creadas ({len(tables)}):")
            for table in tables:
                print(f"  - {table[0]}")
            
            cursor.close()
            connection.close()
            print("\n🚀 ¡Ya puedes ejecutar la aplicación con 'python run.py'!")
            
    except Error as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print(" Creación de Base de Datos eID")
    print("=" * 60)
    create_database()
