from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use Render PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set. "
        "Please configure it with your PostgreSQL connection string."
    )

print(f"Connecting to PostgreSQL...")

# Use psycopg (not psycopg2) for Python 3.13 compatibility
if DATABASE_URL.startswith('postgresql://'):
    DATABASE_URL = DATABASE_URL.replace('postgresql://', 'postgresql+psycopg://', 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections every 5 minutes
    pool_timeout=20,   # Wait up to 20s for a connection
    pool_size=15,      # Larger base pool for concurrent requests
    max_overflow=10,   # Allow up to 25 total connections under load
    connect_args={
        "connect_timeout": 10,
        "application_name": "minore_barbershop"
    }
)
print("✅ Using PostgreSQL database only")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()