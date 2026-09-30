from sqlalchemy import text

from app.database import SessionLocal

db = SessionLocal()

try:
    result = db.execute(text("SELECT DATABASE();"))
    print(result.fetchone())

    print("✅ Connected successfully!")

finally:
    db.close()