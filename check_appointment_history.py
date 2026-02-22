"""
Quick script to check appointment history for a specific client
"""
from database_postgres import SessionLocal
import models

db = SessionLocal()

# Search for Sami's appointments
client_name = "Sami"
appointments = db.query(models.Appointment).filter(
    models.Appointment.client_name.ilike(f"%{client_name}%")
).order_by(models.Appointment.appointment_time.desc()).all()

print(f"\n=== Appointments for '{client_name}' ===\n")
for apt in appointments:
    print(f"ID: {apt.id}")
    print(f"Client: {apt.client_name}")
    print(f"Barber: {apt.barber.name if apt.barber else 'Unknown'}")
    print(f"Time: {apt.appointment_time}")
    print(f"Service: {apt.service.name if apt.service else 'Unknown'}")
    print(f"Status: {apt.status}")
    print(f"Created: {apt.created_at if hasattr(apt, 'created_at') else 'N/A'}")
    print(f"Is Random: {apt.is_random}")
    print("-" * 50)

db.close()
