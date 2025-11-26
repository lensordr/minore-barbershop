from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use Render PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    # Render PostgreSQL URL
    DATABASE_URL = "postgresql://minore_barbershop_production_user:wpxw9iKAdGi4BFyXabqHYl9hSxkdwEYB@dpg-d4jijreuk2gs73bm33vg-a.frankfurt-postgres.render.com/minore_barbershop_production"

print(f"Connecting to PostgreSQL...")

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_timeout=20,
        max_overflow=0,
        connect_args={
            "connect_timeout": 5,
            "application_name": "minore_barbershop"
        }
    )
    # Test connection
    with engine.connect() as conn:
        from sqlalchemy import text
        conn.execute(text("SELECT 1")).fetchone()
    print("✅ PostgreSQL connected")
except Exception as e:
    print(f"❌ PostgreSQL failed: {e}")
    import traceback
    traceback.print_exc()
    print("🔄 Using SQLite fallback")
    engine = create_engine(
        "sqlite:///./barbershop.db",
        connect_args={"check_same_thread": False}
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()