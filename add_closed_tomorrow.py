#!/usr/bin/env python3
"""Migration script to add closed_tomorrow column to barbers table"""

from database_postgres import get_db
from sqlalchemy import text


def add_closed_tomorrow_column():
    """Add closed_tomorrow column to barbers table"""
    db = next(get_db())

    try:
        db.execute(
            text("ALTER TABLE barbers ADD COLUMN closed_tomorrow INTEGER DEFAULT 0")
        )
        db.commit()
        print("✅ Added closed_tomorrow column to barbers table")
    except Exception as e:
        if "already exists" in str(e) or "duplicate column" in str(e).lower():
            print("✅ closed_tomorrow column already exists")
        else:
            print(f"❌ Error adding column: {e}")
            db.rollback()

    db.close()


if __name__ == "__main__":
    print("Adding closed_tomorrow column to barbers table...")
    add_closed_tomorrow_column()
    print("Migration completed!")
