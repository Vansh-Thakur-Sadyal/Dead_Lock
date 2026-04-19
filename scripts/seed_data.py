import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.db.models import Faculty, User, Query
from app.api.auth import hash_password
from scripts.generate_data import faculty_data, student_data, sample_queries
from datetime import datetime

def seed():
    db = SessionLocal()
    try:
        # Seed faculty
        fac_count = 0
        for f in faculty_data:
            existing = db.query(Faculty).filter(Faculty.name == f["name"]).first()
            if not existing:
                faculty = Faculty(**f)
                db.add(faculty)
                fac_count += 1
        db.commit()
        print(f"✅ Seeded {fac_count} faculty records.")

        # Seed faculty users
        for f in faculty_data:
            existing = db.query(User).filter(User.email == f["email"]).first()
            if not existing:
                user = User(
                    name=f["name"],
                    email=f["email"],
                    hashed_password=hash_password("password123"),
                    role="faculty"
                )
                db.add(user)
        db.commit()
        print(f"✅ Seeded faculty user accounts.")

        # Seed students
        stu_count = 0
        for s in student_data:
            existing = db.query(User).filter(User.email == s["email"]).first()
            if not existing:
                user = User(
                    name=s["name"],
                    email=s["email"],
                    hashed_password=hash_password(s["password"]),
                    role="student"
                )
                db.add(user)
                stu_count += 1
        db.commit()
        print(f"✅ Seeded {stu_count} student accounts.")

        # Seed queries
        q_count = 0
        for q in sample_queries:
            query = Query(
                original_query=q["original_query"],
                refined_query=q["refined_query"],
                domain=q["domain"],
                level=q["level"],
                student_email=q["student_email"],
                assigned_faculty=q.get("assigned_faculty"),
                status=q.get("status", "pending"),
                faculty_response=q.get("faculty_response"),
                timestamp=datetime.utcnow()
            )
            db.add(query)
            q_count += 1
        db.commit()
        print(f"✅ Seeded {q_count} sample queries.")

    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()