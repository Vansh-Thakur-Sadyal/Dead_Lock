from sqlalchemy.orm import Session
from app.db.crud import get_query, update_query_status, escalate_query
from app.utils.constants import RESPONSE_TIMEOUT_SECONDS
from datetime import datetime

def check_query_timeout(db: Session, query_id: int) -> bool:
    q = get_query(db, query_id)
    if not q:
        return False
    elapsed = (datetime.utcnow() - q.timestamp).total_seconds()
    return elapsed > RESPONSE_TIMEOUT_SECONDS

def mark_resolved(db: Session, query_id: int):
    update_query_status(db, query_id, "resolved")