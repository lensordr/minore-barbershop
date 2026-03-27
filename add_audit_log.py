"""
Add audit logging to track appointment changes
"""
from database_postgres import SessionLocal, engine
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class AppointmentAuditLog(Base):
    __tablename__ = "appointment_audit_log"
    
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, index=True)
    action = Column(String(50))  # created, updated, cancelled, completed
    changed_by = Column(String(100))  # admin, client, system
    changes = Column(Text)  # JSON string of what changed
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create the audit log table
print("Creating appointment_audit_log table...")
Base.metadata.create_all(bind=engine)
print("✅ Audit log table created successfully!")
