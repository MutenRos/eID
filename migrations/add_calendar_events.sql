-- Migración: Sistema de calendario con eventos y recordatorios
-- Fecha: 2025-11-09

-- Tabla principal de eventos
CREATE TABLE IF NOT EXISTS calendar_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME NOT NULL,
    event_type ENUM('meeting', 'birthday', 'task', 'reminder', 'other') DEFAULT 'other',
    color VARCHAR(7) DEFAULT '#3b82f6',
    location VARCHAR(255),
    reminder_minutes INT DEFAULT 15,
    all_day BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_dates (user_id, start_datetime, end_datetime),
    INDEX idx_start_date (start_datetime)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de participantes (contactos asignados a eventos)
CREATE TABLE IF NOT EXISTS event_participants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT NOT NULL,
    contact_user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES calendar_events(id) ON DELETE CASCADE,
    FOREIGN KEY (contact_user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_participant (event_id, contact_user_id),
    INDEX idx_event (event_id),
    INDEX idx_contact (contact_user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar evento de ejemplo para usuario 1
INSERT INTO calendar_events (user_id, title, description, start_datetime, end_datetime, event_type, color, location, reminder_minutes)
VALUES (
    1,
    'Reunión de ejemplo',
    'Este es un evento de prueba para demostrar el calendario',
    DATE_ADD(NOW(), INTERVAL 1 DAY),
    DATE_ADD(NOW(), INTERVAL 1 DAY + INTERVAL 1 HOUR),
    'meeting',
    '#3b82f6',
    'Oficina',
    30
);
