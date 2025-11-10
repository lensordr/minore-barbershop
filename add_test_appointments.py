from sqlalchemy.orm import sessionmaker
import models, crud
from datetime import datetime, timedelta

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=models.engine)
db = SessionLocal()

# Add some test appointments for today
today = datetime.now().date()
test_appointments = [
    {
        "client_name": "John Smith",
        "phone": "+1234567890",
        "service_id": 1,  # Classic Haircut
        "barber_id": 1,   # Marco Silva
        "time": "10:00"
    },
    {
        "client_name": "Maria Garcia",
        "phone": "+1234567891",
        "service_id": 3,  # Hair + Beard
        "barber_id": 2,   # Antonio Rodriguez
        "time": "11:30"
    },
    {
        "client_name": "David Johnson",
        "phone": "+1234567892",
        "service_id": 2,  # Beard Trim
        "barber_id": 1,   # Marco Silva
        "time": "14:00"
    },
    {
        "client_name": "Sarah Wilson",
        "phone": "+1234567893",
        "service_id": 4,  # Shampoo & Style
        "barber_id": 3,   # Carlos Mendez
        "time": "15:30"
    }
]

for apt in test_appointments:
    appointment_datetime = f"{today}T{apt['time']}:00"
    crud.create_appointment(
        db, 
        apt["client_name"], 
        apt["phone"], 
        apt["service_id"], 
        apt["barber_id"], 
        appointment_datetime
    )

db.close()
print("Test appointments added successfully!")
print("You can now test the checkout functionality in the admin dashboard.")