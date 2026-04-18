from sqlalchemy.orm import Session
from app.db.crud import get_all_faculty

def get_faculty_list(db: Session) -> list:
    return get_all_faculty(db)