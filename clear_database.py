from sqlalchemy.orm import sessionmaker
import models

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=models.engine)
db = SessionLocal()

try:
    # Clear all data from tables (in order to respect foreign key constraints)
    db.query(models.Appointment).delete()
    db.query(models.DailyRevenue).delete()
    db.query(models.MonthlyRevenue).delete()
    db.query(models.Service).delete()
    db.query(models.Barber).delete()
    db.query(models.Schedule).delete()
    
    # Commit the changes
    db.commit()
    
    print("✅ Database cleared successfully!")
    print("All barbers, services, appointments, and revenue data have been removed.")
    print("The database schema is preserved and ready for manual data entry.")
    
except Exception as e:
    db.rollback()
    print(f"❌ Error clearing database: {e}")
    
finally:
    db.close()