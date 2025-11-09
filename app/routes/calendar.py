"""
Rutas para el calendario
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.calendar_event import CalendarEvent
from app.models.contact import Contact
from datetime import datetime

bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@bp.route('/')
@login_required
def index():
    """Vista principal del calendario"""
    # Obtener contactos para el selector de participantes
    contacts = Contact.get_accepted(current_user.id)
    event_types = CalendarEvent.get_event_types()
    return render_template('calendar/index.html', 
                         contacts=contacts, 
                         event_types=event_types)

@bp.route('/events/json')
@login_required
def get_events_json():
    """API: Obtener eventos en formato JSON para FullCalendar"""
    start = request.args.get('start')
    end = request.args.get('end')
    
    if start and end:
        start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
        events = CalendarEvent.get_by_date_range(current_user.id, start_date, end_date)
    else:
        events = CalendarEvent.get_by_user(current_user.id)
    
    return jsonify([event.to_dict() for event in events])

@bp.route('/events/create', methods=['POST'])
@login_required
def create_event():
    """Crear nuevo evento"""
    try:
        data = request.get_json() if request.is_json else request.form
        
        # Crear evento
        event = CalendarEvent(
            user_id=current_user.id,
            title=data.get('title'),
            description=data.get('description'),
            start_datetime=datetime.fromisoformat(data.get('start').replace('Z', '')),
            end_datetime=datetime.fromisoformat(data.get('end').replace('Z', '')),
            event_type=data.get('type', 'other'),
            color=data.get('color', '#3b82f6'),
            location=data.get('location'),
            reminder_minutes=int(data.get('reminder', 15)),
            all_day=data.get('allDay', False)
        )
        
        event_id = event.save()
        
        # Agregar participantes si los hay
        participants = data.get('participants', [])
        if isinstance(participants, str):
            participants = participants.split(',') if participants else []
        
        for participant_id in participants:
            if participant_id:
                event.add_participant(int(participant_id))
        
        if request.is_json:
            return jsonify({'success': True, 'id': event_id, 'event': event.to_dict()})
        else:
            flash('Evento creado correctamente', 'success')
            return redirect(url_for('calendar.index'))
            
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        else:
            flash(f'Error al crear evento: {str(e)}', 'error')
            return redirect(url_for('calendar.index'))

@bp.route('/events/<int:event_id>/edit', methods=['POST'])
@login_required
def edit_event(event_id):
    """Editar evento existente"""
    try:
        event = CalendarEvent.get_by_id(event_id)
        
        if not event or event.user_id != current_user.id:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Evento no encontrado'}), 404
            flash('Evento no encontrado', 'error')
            return redirect(url_for('calendar.index'))
        
        data = request.get_json() if request.is_json else request.form
        
        # Actualizar campos
        event.title = data.get('title', event.title)
        event.description = data.get('description', event.description)
        event.start_datetime = datetime.fromisoformat(data.get('start').replace('Z', ''))
        event.end_datetime = datetime.fromisoformat(data.get('end').replace('Z', ''))
        event.event_type = data.get('type', event.event_type)
        event.color = data.get('color', event.color)
        event.location = data.get('location', event.location)
        event.reminder_minutes = int(data.get('reminder', event.reminder_minutes))
        event.all_day = data.get('allDay', event.all_day)
        
        event.save()
        
        # Actualizar participantes
        if 'participants' in data:
            # Eliminar participantes actuales
            current_participants = event.get_participants()
            for p in current_participants:
                event.remove_participant(p['id'])
            
            # Agregar nuevos participantes
            participants = data.get('participants', [])
            if isinstance(participants, str):
                participants = participants.split(',') if participants else []
            
            for participant_id in participants:
                if participant_id:
                    event.add_participant(int(participant_id))
        
        if request.is_json:
            return jsonify({'success': True, 'event': event.to_dict()})
        else:
            flash('Evento actualizado correctamente', 'success')
            return redirect(url_for('calendar.index'))
            
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        else:
            flash(f'Error al actualizar evento: {str(e)}', 'error')
            return redirect(url_for('calendar.index'))

@bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    """Eliminar evento"""
    try:
        event = CalendarEvent.get_by_id(event_id)
        
        if not event or event.user_id != current_user.id:
            if request.is_json:
                return jsonify({'success': False, 'error': 'Evento no encontrado'}), 404
            flash('Evento no encontrado', 'error')
            return redirect(url_for('calendar.index'))
        
        event.delete()
        
        if request.is_json:
            return jsonify({'success': True})
        else:
            flash('Evento eliminado correctamente', 'success')
            return redirect(url_for('calendar.index'))
            
    except Exception as e:
        if request.is_json:
            return jsonify({'success': False, 'error': str(e)}), 400
        else:
            flash(f'Error al eliminar evento: {str(e)}', 'error')
            return redirect(url_for('calendar.index'))

@bp.route('/events/<int:event_id>')
@login_required
def get_event(event_id):
    """Obtener detalles de un evento específico"""
    event = CalendarEvent.get_by_id(event_id)
    
    if not event or event.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Evento no encontrado'}), 404
    
    return jsonify({'success': True, 'event': event.to_dict()})

@bp.route('/upcoming')
@login_required
def upcoming():
    """Obtener eventos próximos (para dashboard/widget)"""
    days = request.args.get('days', 7, type=int)
    events = CalendarEvent.get_upcoming(current_user.id, days)
    return jsonify([event.to_dict() for event in events])
