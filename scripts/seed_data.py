import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import Faculty
from scripts.generate_data import faculty_data

def seed():
    db = SessionLocal()
    try:
        count = 0
        for f in faculty_data:
            existing = db.query(Faculty).filter(Faculty.name == f["name"]).first()
            if not existing:
                faculty = Faculty(**f)
                db.add(faculty)
                count += 1
        db.commit()
        print(f"✅ Seeded {count} faculty records.")
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()