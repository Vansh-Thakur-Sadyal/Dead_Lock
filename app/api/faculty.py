from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import get_all_faculty

router = APIRouter()

@router.get("/faculty")
def list_faculty(db: Session = Depends(get_db)):
    faculty = get_all_faculty(db)
    return [
        {
            "name": f.name,
            "email": f.email,
            "domains": f.domains,
            "domain_scores": f.domain_scores,
            "active_queries": f.active_queries
        }
        for f in faculty
    ]