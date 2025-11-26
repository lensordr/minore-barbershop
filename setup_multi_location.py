#!/usr/bin/env python3
from sqlalchemy.orm import Session
from database_postgres import engine, SessionLocal
from models import Base, Barber, Service
import bcrypt

def setup_database():
    """Create tables and populate with data for both locations"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Admin login is hardcoded in main.py (admin/minore123)
        print("✅ Admin login: admin/minore123")
        
        # MALLORCA LOCATION (location_id = 1)
        mallorca_barbers = [
            {"name": "Marco Silva", "location_id": 1},
            {"name": "Antonio Rodriguez", "location_id": 1},
            {"name": "Carlos Mendez", "location_id": 1}
        ]
        
        mallorca_services = [
            {"name": "Classic Haircut", "price": 25.0, "duration": 30, "location_id": 1},
            {"name": "Beard Trim", "price": 15.0, "duration": 20, "location_id": 1},
            {"name": "Hair + Beard", "price": 35.0, "duration": 45, "location_id": 1},
            {"name": "Buzz Cut", "price": 20.0, "duration": 15, "location_id": 1},
            {"name": "Fade Cut", "price": 30.0, "duration": 40, "location_id": 1}
        ]
        
        # CONCELL LOCATION (location_id = 2)
        concell_barbers = [
            {"name": "Miguel Torres", "location_id": 2},
            {"name": "David Lopez", "location_id": 2},
            {"name": "Rafael Santos", "location_id": 2}
        ]
        
        concell_services = [
            {"name": "Premium Cut", "price": 28.0, "duration": 35, "location_id": 2},
            {"name": "Beard Styling", "price": 18.0, "duration": 25, "location_id": 2},
            {"name": "Complete Package", "price": 40.0, "duration": 50, "location_id": 2},
            {"name": "Quick Trim", "price": 22.0, "duration": 20, "location_id": 2},
            {"name": "Deluxe Fade", "price": 32.0, "duration": 45, "location_id": 2}
        ]
        
        # Add Mallorca barbers
        for barber_data in mallorca_barbers:
            existing = db.query(Barber).filter(
                Barber.name == barber_data["name"], 
                Barber.location_id == barber_data["location_id"]
            ).first()
            if not existing:
                barber = Barber(**barber_data)
                db.add(barber)
        
        # Add Concell barbers
        for barber_data in concell_barbers:
            existing = db.query(Barber).filter(
                Barber.name == barber_data["name"], 
                Barber.location_id == barber_data["location_id"]
            ).first()
            if not existing:
                barber = Barber(**barber_data)
                db.add(barber)
        
        # Add Mallorca services
        for service_data in mallorca_services:
            existing = db.query(Service).filter(
                Service.name == service_data["name"], 
                Service.location_id == service_data["location_id"]
            ).first()
            if not existing:
                service = Service(**service_data)
                db.add(service)
        
        # Add Concell services
        for service_data in concell_services:
            existing = db.query(Service).filter(
                Service.name == service_data["name"], 
                Service.location_id == service_data["location_id"]
            ).first()
            if not existing:
                service = Service(**service_data)
                db.add(service)
        
        db.commit()
        print("✅ Database setup complete!")
        print("📍 Mallorca: 3 barbers, 5 services")
        print("📍 Concell: 3 barbers, 5 services")
        print("👤 Admin login: admin / minore123")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()