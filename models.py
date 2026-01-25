from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String, unique=True, index=True)  # Unique phone number
    name = Column(String)
    email = Column(String, default="")
    created_at = Column(DateTime)
    
    appointments = relationship("Appointment", back_populates="client")

class Barber(Base):
    __tablename__ = "barbers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    active = Column(Integer, default=1)  # 1=active, 0=closed
    location_id = Column(Integer, default=1)  # 1=mallorca, 2=concell
    
    appointments = relationship("Appointment", back_populates="barber")

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    duration = Column(Integer)  # minutes
    price = Column(Float)
    location_id = Column(Integer, default=1)  # 1=mallorca, 2=concell
    
    appointments = relationship("Appointment", back_populates="service")

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"))  # Link to client
    appointment_time = Column(DateTime)
    barber_id = Column(Integer, ForeignKey("barbers.id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    custom_price = Column(Float, default=None)  # Override service price
    custom_duration = Column(Integer, default=None)  # Override service duration
    is_random = Column(Integer, default=0)  # 1 if randomly assigned
    is_online = Column(Integer, default=0)  # 1 if booked online by client
    cancel_token = Column(String, default="")
    
    # Legacy fields for backward compatibility
    client_name = Column(String, default="")
    phone = Column(String, default="")
    email = Column(String, default="")
    location_id = Column(Integer, default=1)
    
    client = relationship("Client", back_populates="appointments")
    barber = relationship("Barber", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")

class Schedule(Base):
    __tablename__ = "schedule"
    
    id = Column(Integer, primary_key=True, index=True)
    start_hour = Column(Integer, default=11)  # 11 AM
    end_hour = Column(Integer, default=19)    # 7 PM
    is_open = Column(Integer, default=1)      # 1=open, 0=closed (master toggle)
    monday = Column(Integer, default=1)       # 1=open, 0=closed
    tuesday = Column(Integer, default=1)
    wednesday = Column(Integer, default=1)
    thursday = Column(Integer, default=1)
    friday = Column(Integer, default=1)
    saturday = Column(Integer, default=1)
    sunday = Column(Integer, default=0)

class MonthlyRevenue(Base):
    __tablename__ = "monthly_revenue"
    
    id = Column(Integer, primary_key=True, index=True)
    barber_id = Column(Integer, ForeignKey("barbers.id"))
    year = Column(Integer)
    month = Column(Integer)
    revenue = Column(Float, default=0.0)
    appointments_c