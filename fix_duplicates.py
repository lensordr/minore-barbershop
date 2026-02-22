"""
Find and fix duplicate appointments before adding unique constraint
"""
from database_postgres import SessionLocal
from sqlalchemy import text
import models

db = SessionLocal()

# Find duplicates
print("🔍 Searching for duplicate appointments...")
print("=" * 70)

duplicates = db.execute(text("""
    SELECT barber_id, appointment_time, location_id, COUNT(*) as count
    FROM appointments
    WHERE status != 'cancelled'
    GROUP BY barber_id, appointment_time, location_id
    HAVING COUNT(*) > 1
""")).fetchall()

if not duplicates:
    print("✅ No duplicates found!")
else:
    print(f"⚠️  Found {len(duplicates)} duplicate slots:\n")
    
    for dup in duplicates:
        barber_id, apt_time, location_id, count = dup
        print(f"Barber {barber_id}, Time: {apt_time}, Location: {location_id} - {count} appointments")
        
        # Get the actual appointments
        appointments = db.query(models.Appointment).filter(
            models.Appointment.barber_id == barber_id,
            models.Appointment.appointment_time == apt_time,
            models.Appointment.location_id == location_id,
            models.Appointment.status != 'cancelled'
        ).order_by(models.Appointment.id).all()
        
        print(f"  Appointments:")
        for apt in appointments:
            print(f"    ID: {apt.id}, Client: {apt.client_name}, Status: {apt.status}, Created: {apt.created_at if hasattr(apt, 'created_at') else 'N/A'}")
        
        # Keep the first one, cancel the rest
        if len(appointments) > 1:
            keep = appointments[0]
            cancel = appointments[1:]
            
            print(f"\n  ✅ Keeping: ID {keep.id} ({keep.client_name})")
            print(f"  ❌ Cancelling: {[apt.id for apt in cancel]}")
            
            for apt in cancel:
                apt.status = 'cancelled'
            
            db.commit()
            print(f"  ✅ Fixed!\n")

print("=" * 70)
print("✅ All duplicates resolved!")
db.close()
