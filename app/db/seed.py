from sqlalchemy.orm import Session
from app.db.models import Faculty

def seed_faculty(db: Session, faculty_list: list):
    for f in faculty_list:
        existing = db.query(Faculty).filter(Faculty.name == f["name"]).first()
        if not existing:
            faculty = Faculty(**f)
            db.add(faculty)
    db.commit()