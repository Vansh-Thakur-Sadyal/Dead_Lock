from sqlalchemy.orm import Session
from app.db.models import Faculty, Query, Feedback
from datetime import datetime

# --- Faculty ---
def get_all_faculty(db: Session):
    return db.query(Faculty).all()

def get_faculty_by_name(db: Session, name: str):
    return db.query(Faculty).filter(Faculty.name == name).first()

def update_faculty_domain_score(db: Session, name: str, domain: str, new_score: float):
    faculty = get_faculty_by_name(db, name)
    if faculty:
        scores = faculty.domain_scores or {}
        scores[domain] = round(max(0.0, min(1.0, new_score)), 4)
        faculty.domain_scores = scores
        db.commit()

def increment_active_queries(db: Session, name: str):
    faculty = get_faculty_by_name(db, name)
    if faculty:
        faculty.active_queries += 1
        db.commit()

def decrement_active_queries(db: Session, name: str):
    faculty = get_faculty_by_name(db, name)
    if faculty:
        faculty.active_queries = max(0, faculty.active_queries - 1)
        db.commit()

# --- Query ---
def create_query(db: Session, original: str, refined: str = None, domain: str = None, level: str = None, student_email: str = None, papers: list = None):
    q = Query(
        original_query=original,
        refined_query=refined,
        domain=domain,
        level=level,
        student_email=student_email,
        research_papers=papers or []
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

def get_query(db: Session, query_id: int):
    return db.query(Query).filter(Query.id == query_id).first()

def update_query_status(db: Session, query_id: int, status: str, faculty: str = None):
    q = get_query(db, query_id)
    if q:
        q.status = status
        if faculty:
            q.assigned_faculty = faculty
        db.commit()

def update_query_attempt(db: Session, query_id: int):
    q = get_query(db, query_id)
    if q:
        q.attempt += 1
        db.commit()

def escalate_query(db: Session, query_id: int):
    q = get_query(db, query_id)
    if q:
        q.escalation_level += 1
        q.status = "escalated"
        db.commit()

# --- Feedback ---
def create_feedback(db: Session, query_id: int, faculty_name: str, feedback: str):
    f = Feedback(query_id=query_id, faculty_name=faculty_name, feedback=feedback)
    db.add(f)
    db.commit()
    db.refresh(f)
    return f

def get_feedback_for_faculty(db: Session, faculty_name: str):
    return db.query(Feedback).filter(Feedback.faculty_name == faculty_name).all()