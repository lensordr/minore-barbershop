"""
View recent appointment audit logs
"""
from database_postgres import SessionLocal
import models

db = SessionLocal()

# Get recent audit logs
logs = db.query(models.AppointmentAuditLog).order_by(
    models.AppointmentAuditLog.timestamp.desc()
).limit(50).all()

print(f"\n=== Recent Appointment Changes (Last 50) ===\n")
for log in logs:
    appointment = db.query(models.Appointment).filter(models.Appointment.id == log.appointment_id).first()
    client_name = appointment.client_name if appointment else "Unknown"
    
    print(f"[{log.timestamp}] {log.action.upper()}")
    print(f"  Appointment ID: {log.appointment_id} ({client_name})")
    print(f"  Changed by: {log.changed_by}")
    print(f"  Changes: {log.changes}")
    print("-" * 70)

db.close()
