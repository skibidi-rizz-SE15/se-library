import os
from sqlmodel import create_engine, text

database_url = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydatabase")

try:
    engine = create_engine(database_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database connected successfully!" if result.scalar() == 1 else "Database connection failed.")
except Exception as e:
    print(f"Database connection error: {e}")