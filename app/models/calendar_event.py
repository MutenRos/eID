"""
Modelo para eventos de calendario
"""
from app.database import db
from datetime import datetime, timedelta

class CalendarEvent:
    """Modelo de evento de calendario"""
    
    def __init__(self, id=None, user_id=None, title=None, description=None,
                 start_datetime=None, end_datetime=None, event_type='other',
                 color='#3b82f6', location=None, reminder_minutes=15,
                 all_day=False, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.event_type = event_type
        self.color = color
        self.location = location
        self.reminder_minutes = reminder_minutes
        self.all_day = all_day
        self.created_at = created_at
        self.updated_at = updated_at
        
    def save(self):
        """Guardar o actualizar evento"""
        if self.id:
            # Actualizar evento existente
            query = """
                UPDATE calendar_events 
                SET title = %s, description = %s, start_datetime = %s, 
                    end_datetime = %s, event_type = %s, color = %s, 
                    location = %s, reminder_minutes = %s, all_day = %s
                WHERE id = %s
            """
            db.execute_query(query, (
                self.title, self.description, self.start_datetime,
                self.end_datetime, self.event_type, self.color,
                self.location, self.reminder_minutes, self.all_day, self.id
            ))
        else:
            # Crear nuevo evento
            query = """
                INSERT INTO calendar_events 
                (user_id, title, description, start_datetime, end_datetime, 
                 event_type, color, location, reminder_minutes, all_day)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            result = db.execute_query(query, (
                self.user_id, self.title, self.description, self.start_datetime,
                self.end_datetime, self.event_type, self.color, self.location,
                self.reminder_minutes, self.all_day
            ))
            self.id = result
        return self.id
    
    def delete(self):
        """Eliminar evento"""
        db.execute_query("DELETE FROM calendar_events WHERE id = %s", (self.id,))
    
    def add_participant(self, contact_user_id):
        """Agregar un contacto como participante del evento"""
        try:
            db.execute_query(
                "INSERT INTO event_participants (event_id, contact_user_id) VALUES (%s, %s)",
                (self.id, contact_user_id)
            )
            return True
        except:
            # Ya existe o error
            return False
    
    def remove_participant(self, contact_user_id):
        """Eliminar un participante del evento"""
        db.execute_query(
            "DELETE FROM event_participants WHERE event_id = %s AND contact_user_id = %s",
            (self.id, contact_user_id)
        )
    
    def get_participants(self):
        """Obtener lista de participantes del evento"""
        query = """
            SELECT u.id, u.username, u.full_name, u.profile_image
            FROM event_participants ep
            JOIN users u ON ep.contact_user_id = u.id
            WHERE ep.event_id = %s
        """
        return db.fetch_all(query, (self.id,))
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'start': self.start_datetime.isoformat() if self.start_datetime else None,
            'end': self.end_datetime.isoformat() if self.end_datetime else None,
            'allDay': self.all_day,
            'backgroundColor': self.color,
            'borderColor': self.color,
            'extendedProps': {
                'type': self.event_type,
                'location': self.location,
                'reminder': self.reminder_minutes,
                'participants': self.get_participants() if self.id else []
            }
        }
    
    @staticmethod
    def get_by_id(event_id):
        """Obtener evento por ID"""
        data = db.fetch_one("SELECT * FROM calendar_events WHERE id = %s", (event_id,))
        if data:
            return CalendarEvent(**data)
        return None
    
    @staticmethod
    def get_by_user(user_id):
        """Obtener todos los eventos de un usuario"""
        query = "SELECT * FROM calendar_events WHERE user_id = %s ORDER BY start_datetime ASC"
        events_data = db.fetch_all(query, (user_id,))
        return [CalendarEvent(**data) for data in events_data]
    
    @staticmethod
    def get_by_date_range(user_id, start_date, end_date):
        """Obtener eventos en un rango de fechas"""
        query = """
            SELECT * FROM calendar_events 
            WHERE user_id = %s 
            AND start_datetime <= %s 
            AND end_datetime >= %s
            ORDER BY start_datetime ASC
        """
        events_data = db.fetch_all(query, (user_id, end_date, start_date))
        return [CalendarEvent(**data) for data in events_data]
    
    @staticmethod
    def get_upcoming(user_id, days=7):
        """Obtener eventos próximos"""
        start = datetime.now()
        end = start + timedelta(days=days)
        query = """
            SELECT * FROM calendar_events 
            WHERE user_id = %s 
            AND start_datetime >= %s 
            AND start_datetime <= %s
            ORDER BY start_datetime ASC
        """
        events_data = db.fetch_all(query, (user_id, start, end))
        return [CalendarEvent(**data) for data in events_data]
    
    @staticmethod
    def get_event_types():
        """Obtener tipos de eventos disponibles"""
        return [
            {'value': 'meeting', 'label': 'Reunión', 'icon': '👥', 'color': '#3b82f6'},
            {'value': 'birthday', 'label': 'Cumpleaños', 'icon': '🎂', 'color': '#ec4899'},
            {'value': 'task', 'label': 'Tarea', 'icon': '✅', 'color': '#10b981'},
            {'value': 'reminder', 'label': 'Recordatorio', 'icon': '⏰', 'color': '#f59e0b'},
            {'value': 'other', 'label': 'Otro', 'icon': '📌', 'color': '#8b5cf6'}
        ]
