#!/usr/bin/env python3
"""
Add client accounts system to existing database
"""
from sqlalchemy import create_engine, text
from database_postgres import engine
import os

def add_client_accounts():
    """Add clients table and update appointments table"""
    
    with engine.connect() as conn:
        # Create clients table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                phone VARCHAR UNIQUE NOT NULL,
                name VARCHAR,
                email VARCHAR DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        
        # Add client_id column to appointments (nullable for migration)
        try:
            conn.execute(text("""
                ALTER TABLE appointments 
                ADD COLUMN client_id INTEGER REFERENCES clients(id) ON DELETE CASCADE;
            """))
        except Exception as e:
            print(f"Column client_id might already exist: {e}")
        
        # Migrate existing appointments to client accounts
        conn.execute(text("""
            INSERT INTO clients (phone, name, email)
            SELECT DISTINCT 
                COALESCE(phone, 'unknown'), 
                COALESCE(client_name, 'Unknown Client'),
                COALESCE(email, '')
            FROM appointments 
            WHERE phone IS NOT NULL AND phone != ''
            ON CONFLICT (phone) DO NOTHING;
        """))
        
        # Update appointments with client_id
        conn.execute(text("""
            UPDATE appointments 
            SET client_id = clients.id
            FROM clients 
            WHERE appointments.phone = clients.phone;
        """))
        
        conn.commit()
        print("✅ Client accounts system added successfully!")

if __name__ == "__main__":
    add_client_accounts()