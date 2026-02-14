-- Script de creación de base de datos eID para MySQL
-- Ejecutar este script antes de iniciar la aplicación

CREATE DATABASE IF NOT EXISTS eid CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE eid;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL,
    friend_code VARCHAR(12) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    bio TEXT,
    avatar VARCHAR(200) DEFAULT 'default.png',
    website VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_friend_code (friend_code)
) ENGINE=InnoDB;

-- Tabla de enlaces a redes sociales
CREATE TABLE IF NOT EXISTS social_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    platform VARCHAR(50) NOT NULL,
    username VARCHAR(100) NOT NULL,
    url VARCHAR(500) NOT NULL,
    is_visible BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_platform (user_id, platform)
) ENGINE=InnoDB;

-- Tabla de contactos
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
) ENGINE=InnoDB;

-- Tabla de mensajes
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
) ENGINE=InnoDB;

-- Datos de prueba (opcional)
-- Usuario de prueba: dario / password123
INSERT INTO users (username, email, password_hash, full_name, bio) VALUES
('dario', 'dario@eid.com', 'scrypt:32768:8:1$LvZ8qW9K7YfXnGjP$f3e8c0d1a2b9c4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6', 'Darío Lacal Civera', 'Desarrollador DAM apasionado por la tecnología');

-- Nota: El hash anterior es de ejemplo. Para crear usuarios usa la función de registro.

-- Vista para obtener estadísticas de cada usuario (contactos, mensajes, redes)
CREATE OR REPLACE VIEW user_stats AS
SELECT 
    u.id,
    u.username,
    u.full_name,
    (SELECT COUNT(*) FROM contacts c 
     WHERE (c.user_id = u.id OR c.contact_id = u.id) AND c.status = 'accepted') AS total_contactos,
    (SELECT COUNT(*) FROM messages m 
     WHERE m.sender_id = u.id) AS mensajes_enviados,
    (SELECT COUNT(*) FROM social_links sl 
     WHERE sl.user_id = u.id AND sl.is_visible = TRUE) AS redes_vinculadas,
    u.created_at AS fecha_registro
FROM users u;
