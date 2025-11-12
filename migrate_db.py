from sqlalchemy import text
from models import engine

# Add new columns to existing appointments table
with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE appointments ADD COLUMN custom_price FLOAT"))
        print("Added custom_price column")
    except Exception as e:
        print(f"custom_price column might already exist: {e}")
    
    try:
        conn.execute(text("ALTER TABLE appointments ADD COLUMN custom_duration INTEGER"))
        print("Added custom_duration column")
    except Exception as e:
        print(f"custom_duration column might already exist: {e}")
    
    conn.commit()
    print("Database migration completed!")