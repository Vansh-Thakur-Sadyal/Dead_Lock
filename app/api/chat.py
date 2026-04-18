from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.core.chatbot.orchestrator import handle_query
from app.system.feedback import apply_feedback

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class FeedbackRequest(BaseModel):
    query_id: int
    faculty_name: str
    domain: str
    feedback: str  # "relevant" or "irrelevant"

@router.post("/chat")
async def chat(request: QueryRequest, db: Session = Depends(get_db)):
    result = await handle_query(request.query, db)
    return result

@router.post("/feedback")
def feedback(request: FeedbackRequest, db: Session = Depends(get_db)):
    result = apply_feedback(db, request.query_id, request.faculty_name, request.domain, request.feedback)
    return result