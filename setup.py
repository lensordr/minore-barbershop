from sqlalchemy.orm import sessionmaker
import models, crud

# Create tables
models.Base.metadata.create_all(bind=models.engine)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=models.engine)
db = SessionLocal()

# Add sample barbers
barbers = [
    "Luca",
    "Michele", 
    "Raffaele",
    "Abel",
    "Wendy",
    "Sergio"
]

for barber_name in barbers:
    existing = db.query(models.Barber).filter(models.Barber.name == barber_name).first()
    if not existing:
        crud.create_barber(db, barber_name)

# Add sample services
services = [
    ("Classic Haircut", "Traditional scissor cut with styling", 30, 25.00),
    ("Beard Trim", "Professional beard shaping and trimming", 20, 15.00),
    ("Hair + Beard", "Complete grooming package", 45, 35.00),
    ("Shampoo & Style", "Hair wash and professional styling", 25, 20.00),
    ("Buzz Cut", "Short clipper cut all around", 15, 18.00)
]

for service_name, description, duration, price in services:
    existing = db.query(models.Service).filter(models.Service.name == service_name).first()
    if not existing:
        crud.create_service(db, service_name, duration, price, description)

db.close()
print("Database setup complete!")
print("Sample barbers and services added.")
print("\nTo run the application:")
print("python main.py")
print("\nAccess URLs:")
print("- Customer booking: http://localhost:8000/book")
print("- Admin login: http://localhost:8000/admin/login")
print("- Default admin credentials: admin / minore123")