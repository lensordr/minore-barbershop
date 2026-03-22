"""
Migration: Add performance indexes to appointments table.
Safe to run multiple times (uses IF NOT EXISTS).
"""
from database_postgres import engine
from sqlalchemy import text

def add_indexes():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_appointments_barber_time_status
            ON appointments (barber_id, appointment_time, status)
        """))
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_appointments_location_time
            ON appointments (location_id, appointment_time)
        """))
        conn.commit()
        print("✅ Indexes created (or already existed)")

if __name__ == "__main__":
    add_indexes()
