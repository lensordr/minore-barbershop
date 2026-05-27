from datetime import datetime, timedelta

def create_appointment_grid(db, appointments, schedule, location_id=None, barbers=None):
    """Optimized grid creation - minimal database calls.
    
    Prioritizes online appointments (is_online >= 1) over manual ones (is_online == 0)
    when multiple non-cancelled appointments occupy the same time slot for the same barber.
    This prevents manual appointments from silently hiding online bookings in the grid.
    
    Args:
        db: Database session.
        appointments: List of appointment objects.
        schedule: Schedule object with start_hour and end_hour.
        location_id: Optional location ID for filtering barbers.
        barbers: Optional pre-fetched list of barbers. If provided, skips the
                 internal database query for barbers.
    """
    import crud
    
    # Generate time slots once
    hours = []
    for h in range(schedule.start_hour, schedule.end_hour):
        hours.append(f"{h:02d}:00")
        hours.append(f"{h:02d}:30")
    
    # Use pre-fetched barbers if provided, otherwise query the database
    if barbers is not None:
        all_barbers = barbers
    elif location_id:
        all_barbers = crud.get_barbers_with_revenue_by_location(db, location_id)
    else:
        all_barbers = crud.get_barbers(db)
    
    # Pre-create empty grid structure
    empty_slot = {"type": "empty", "appointment": None, "is_start": False, "span_rows": 1}
    grid = {barber.id: {hour: empty_slot.copy() for hour in hours} for barber in all_barbers}
    
    # Create hour index lookup for faster processing
    hour_index = {hour: idx for idx, hour in enumerate(hours)}
    
    # Fill grid with appointments — prioritize online bookings over manual ones
    # when there's a conflict at the same start time for the same barber.
    for appointment in appointments:
        if appointment.status == "cancelled":
            continue
            
        barber_id = appointment.barber_id
        start_time = appointment.appointment_time.strftime("%H:%M")
        
        if barber_id not in grid or start_time not in hour_index:
            continue
            
        duration = appointment.custom_duration or appointment.service.duration
        slots_needed = (duration + 29) // 30
        
        current_slot = grid[barber_id][start_time]
        
        # If slot already has an appointment, keep the online one (higher priority)
        if current_slot["type"] == "appointment":
            existing_apt = current_slot["appointment"]
            existing_is_online = getattr(existing_apt, "is_online", 0) or 0
            new_is_online = getattr(appointment, "is_online", 0) or 0
            
            # Online appointments (is_online >= 1) take priority over manual (is_online == 0)
            if existing_is_online >= 1 and new_is_online == 0:
                # Existing is online, new is manual — keep existing, skip new
                continue
            elif existing_is_online == 0 and new_is_online >= 1:
                # Existing is manual, new is online — replace with online appointment
                pass  # Fall through to overwrite
            else:
                # Both same type — keep the one with lower ID (created first)
                if existing_apt.id < appointment.id:
                    continue
        
        # Mark starting slot
        grid[barber_id][start_time] = {
            "type": "appointment",
            "appointment": appointment,
            "is_start": True,
            "span_rows": slots_needed
        }
        
        # Mark continuation slots efficiently
        start_idx = hour_index[start_time]
        for i in range(1, min(slots_needed, len(hours) - start_idx)):
            next_slot = hours[start_idx + i]
            grid[barber_id][next_slot] = {
                "type": "continuation",
                "appointment": appointment,
                "is_start": False,
                "span_rows": 1
            }
    
    return {"grid": grid, "hours": hours}