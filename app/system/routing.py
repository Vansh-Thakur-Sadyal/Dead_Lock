from sqlalchemy.orm import Session
from app.db.crud import update_query_status, update_query_attempt, escalate_query, get_query, increment_active_queries, decrement_active_queries
from app.utils.constants import MAX_ATTEMPTS_BEFORE_ESCALATION
from app.utils.logger import get_logger

logger = get_logger(__name__)

def assign_faculty(db: Session, query_id: int, faculty_name: str):
    update_query_status(db, query_id, "routed", faculty=faculty_name)
    increment_active_queries(db, faculty_name)
    logger.info(f"Query {query_id} assigned to {faculty_name}")

def reroute(db: Session, query_id: int, next_faculty: str):
    q = get_query(db, query_id)
    if not q:
        return
    decrement_active_queries(db, q.assigned_faculty)
    update_query_attempt(db, query_id)

    if q.attempt >= MAX_ATTEMPTS_BEFORE_ESCALATION:
        escalate_query(db, query_id)
        logger.warning(f"Query {query_id} escalated")
    else:
        assign_faculty(db, query_id, next_faculty)