from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Query as QueryModel, User
from app.core.auth_deps import require_student
from app.system.routing import assign_faculty

router = APIRouter()

class AssignRequest(BaseModel):
    query_id: int
    faculty_name: str

@router.get("/student/queries")
def get_student_queries(
    db: Session = Depends(get_db),
    user: dict = Depends(require_student)
):
    queries = db.query(QueryModel).filter(
        QueryModel.student_email == user.get("sub")
    ).order_by(QueryModel.timestamp.desc()).all()
    return [
        {
            "query_id": q.id,
            "original_query": q.original_query,
            "refined_query": q.refined_query,
            "domain": q.domain,
            "level": q.level,
            "assigned_faculty": q.assigned_faculty,
            "status": q.status,
            "faculty_response": q.faculty_response,
            "timestamp": q.timestamp
        }
        for q in queries
    ]

@router.get("/student/query/{query_id}")
def get_query_status(
    query_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(require_student)
):
    query = db.query(QueryModel).filter(QueryModel.id == query_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    return {
        "query_id": query.id,
        "original_query": query.original_query,
        "refined_query": query.refined_query,
        "domain": query.domain,
        "level": query.level,
        "assigned_faculty": query.assigned_faculty,
        "status": query.status,
        "faculty_response": query.faculty_response,
        "timestamp": query.timestamp
    }

@router.get("/student/profile")
def student_profile(
    db: Session = Depends(get_db),
    user: dict = Depends(require_student)
):
    student = db.query(User).filter(User.email == user.get("sub")).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "name": student.name,
        "email": student.email,
        "role": student.role,
        "created_at": student.created_at
    }

@router.post("/student/assign")
def assign_query(
    request: AssignRequest,
    db: Session = Depends(get_db),
    user: dict = Depends(require_student)
):
    assign_faculty(db, request.query_id, request.faculty_name)
    return {"message": "Query assigned", "query_id": request.query_id, "faculty": request.faculty_name}