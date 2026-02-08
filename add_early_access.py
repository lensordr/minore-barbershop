#!/usr/bin/env python3
"""
Add early access columns to barbers table
"""

from database_postgres import get_db
from sqlalchemy import text

def add_early_access_columns():
    db = next(get_db())
    
    try:
        # Add early_access_enabled column
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='barbers' AND column_name='early_access_enabled'
        """)).fetchone()
        
        if not result:
            db.execute(text("ALTER TABLE barbers ADD COLUMN early_access_enabled INTEGER DEFAULT 0"))
            print("✅ Added 'early_access_enabled' column")
        else:
            print("✅ 'early_access_enabled' column already exists")
        
        # Add early_access_price_add column
        result = db.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='barbers' AND column_name='early_access_price_add'
        """)).fetchone()
        
        if not result:
            db.execute(text("ALTER TABLE barbers ADD COLUMN early_access_price_add FLOAT DEFAULT 0.0"))
            print("✅ Added 'early_access_price_add' column")
        else:
            print("✅ 'early_access_price_add' column already exists")
            
        db.commit()
        print("✅ Migration completed successfully")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_early_access_columns()
