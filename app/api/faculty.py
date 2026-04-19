from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Query as QueryModel, Faculty
from app.db.crud import get_all_faculty
from app.core.auth_deps import require_faculty

router = APIRouter()

class RespondRequest(BaseModel):
    query_id: int
    response: str

@router.get("/faculty/queries")
def get_faculty_queries(
    domain: str = None,
    level: str = None,
    priority: str = None,  # "escalated" or "normal"
    db: Session = Depends(get_db),
    user: dict = Depends(require_faculty)
):
    faculty_name = user.get("name")

    # Get all queries assigned to this faculty
    q = db.query(QueryModel).filter(QueryModel.assigned_faculty == faculty_name)

    # Filters
    if domain:
        q = q.filter(QueryModel.domain == domain)
    if level:
        q = q.filter(QueryModel.level == level)
    if priority == "escalated":
        q = q.filter(QueryModel.escalation_level > 0)
    elif priority == "normal":
        q = q.filter(QueryModel.escalation_level == 0)

    queries = q.all()

    # Sort: escalated first, then FCFS (oldest first)
    escalated = [x for x in queries if x.escalation_level > 0]
    normal = [x for x in queries if x.escalation_level == 0]
    escalated.sort(key=lambda x: x.timestamp)
    normal.sort(key=lambda x: x.timestamp)

    final = escalated + normal

    return [
        {
            "query_id": q.id,
            "original_query": q.original_query,
            "refined_query": q.refined_query,
            "domain": q.domain,
            "level": q.level,
            "status": q.status,
            "escalated": q.escalation_level > 0,
            "timestamp": q.timestamp,
            "faculty_response": q.faculty_response
        }
        for q in final
    ]

@router.post("/faculty/respond")
def respond_to_query(
    request: RespondRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_faculty)
):
    query = db.query(QueryModel).filter(QueryModel.id == request.query_id).first()
    if not query:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Query not found")

    query.faculty_response = request.response
    query.status = "resolved"
    db.commit()

    return {"message": "Response submitted", "query_id": request.query_id}

@router.get("/faculty/profile")
def faculty_profile(
    db: Session = Depends(get_db),
    user: dict = Depends(require_faculty)
):
    faculty = db.query(Faculty).filter(Faculty.name == user.get("name")).first()
    if not faculty:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Faculty not found")

    return {
        "name": faculty.name,
        "email": faculty.email,
        "domains": faculty.domains,
        "projects": faculty.projects,
        "papers": faculty.papers,
        "domain_scores": faculty.domain_scores,
        "active_queries": faculty.active_queries
    }