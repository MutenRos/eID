-- Migration: Añadir sistema de carpetas para contactos
-- Fecha: 2025-11-09

-- Tabla para carpetas de contactos
CREATE TABLE IF NOT EXISTS contact_folders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    color VARCHAR(20) DEFAULT '#6366f1',
    icon VARCHAR(50) DEFAULT 'folder',
    position INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_folders (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Añadir campo folder_id a tabla contacts
ALTER TABLE contacts 
ADD COLUMN folder_id INT NULL,
ADD FOREIGN KEY (folder_id) REFERENCES contact_folders(id) ON DELETE SET NULL;

-- Crear carpeta por defecto "Todos" para usuarios existentes
INSERT INTO contact_folders (user_id, name, color, icon, position)
SELECT id, 'Todos', '#6366f1', 'users', 0
FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM contact_folders);
