#!/usr/bin/env python3
"""
Add blocked column to clients table
"""

from database_postgres import get_db
from sqlalchemy import text

def add_blocked_column():
    db = next(get_db())
    
    try:
        # Check if column already exists
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='clients' AND column_name='blocked'
        """)).fetchone()
        
        if not result:
            # Add blocked column
            db.execute(text("ALTER TABLE clients ADD COLUMN blocked INTEGER DEFAULT 0"))
            db.commit()
            print("✅ Added 'blocked' column to clients table")
        else:
            print("✅ 'blocked' column already exists")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_blocked_column()