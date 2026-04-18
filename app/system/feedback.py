from sqlalchemy.orm import Session
from app.db.crud import get_faculty_by_name, update_faculty_domain_score, create_feedback
from app.utils.constants import RELEVANT_INCREASE, IRRELEVANT_DECREASE
from app.utils.helpers import clamp

def apply_feedback(db: Session, query_id: int, faculty_name: str, domain: str, feedback: str):
    faculty = get_faculty_by_name(db, faculty_name)
    if not faculty:
        return

    scores = faculty.domain_scores or {}
    current_score = scores.get(domain, 0.5)

    if feedback == "relevant":
        new_score = current_score + RELEVANT_INCREASE * (1 - current_score)
    else:
        new_score = current_score - IRRELEVANT_DECREASE * current_score

    new_score = clamp(new_score)
    update_faculty_domain_score(db, faculty_name, domain, new_score)
    create_feedback(db, query_id, faculty_name, feedback)

    return {"faculty": faculty_name, "domain": domain, "new_score": round(new_score, 4)}