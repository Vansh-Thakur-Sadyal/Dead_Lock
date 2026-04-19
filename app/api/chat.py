from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db.models import (
    Query as QueryModel, User,
    ChatRequest, ChatSession, ChatMessage
)
from app.db.crud import create_query
from app.core.chatbot.rag_controller import get_papers
from app.core.matcher import match_faculty
from app.core.auth_deps import require_student, require_faculty, get_current_user
from app.services.llm import conversational_chat, extract_query_details
from app.system.feedback import apply_feedback

router = APIRouter()

MAX_PENDING_REQUESTS     = 3
CHAT_REQUEST_EXPIRY_MIN  = 10
MAX_ACTIVE_SESSIONS      = 2


# ── Pydantic Schemas ──────────────────────────────────────────────────────────

class ChatMsgIn(BaseModel):
    message: str
    history: list = []  # [{role: "user"|"ai", content: str}]

class ConfirmIn(BaseModel):
    final_query: str
    papers: list = []

class RecommendIn(BaseModel):
    query_id: int

class FeedbackIn(BaseModel):
    query_id: int
    faculty_name: str
    domain: str
    feedback: str  # "relevant" or "irrelevant"

class ChatRequestIn(BaseModel):
    faculty_name: str
    query_id: Optional[int] = None
    topic: Optional[str] = None

class SendMessageIn(BaseModel):
    session_id: int
    content: str


# ── Helper ────────────────────────────────────────────────────────────────────

def expire_old_requests(db: Session):
    db.query(ChatRequest).filter(
        ChatRequest.status == "pending",
        ChatRequest.expires_at < datetime.utcnow()
    ).update({"status": "expired"})
    db.commit()


# ══════════════════════════════════════════════════════════════════════════════
#  PHASE 1 — Conversational Chat
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/chat")
async def chat(request: ChatMsgIn, db: Session = Depends(get_db),
               user: dict = Depends(require_student)):
    result = await conversational_chat(request.message, request.history)
    papers = await get_papers(request.message)
    return {
        "reply":      result.get("reply", ""),
        "is_vague":   result.get("is_vague", True),
        "papers":     papers,
        "topic_hint": result.get("topic_hint", "")
    }


# ══════════════════════════════════════════════════════════════════════════════
#  PHASE 2 — Confirm Query
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/chat/confirm")
async def confirm_chat(request: ConfirmIn, db: Session = Depends(get_db),
                       user: dict = Depends(require_student)):
    details = await extract_query_details(request.final_query)
    q = create_query(
        db,
        original=request.final_query,
        refined=details.get("refined_query", request.final_query),
        domain=details.get("domain", "general"),
        level=details.get("level", "intermediate"),
        student_email=user.get("sub"),
        papers=request.papers
    )
    return {
        "query_id":     q.id,
        "refined_query": details.get("refined_query", request.final_query),
        "domain":       details.get("domain", "general"),
        "level":        details.get("level", "intermediate"),
        "papers":       request.papers
    }


# ══════════════════════════════════════════════════════════════════════════════
#  PHASE 3 — Faculty Recommendations
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/chat/recommend")
async def recommend(request: RecommendIn, db: Session = Depends(get_db),
                    user: dict = Depends(require_student)):
    q = db.query(QueryModel).filter(QueryModel.id == request.query_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Query not found")
    matches = match_faculty(db, q.refined_query or q.original_query, q.domain or "general")
    return {"query_id": request.query_id, "faculty_recommendations": matches}


# ══════════════════════════════════════════════════════════════════════════════
#  RLFF Feedback
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/feedback")
def feedback(request: FeedbackIn, db: Session = Depends(get_db),
             user: dict = Depends(require_faculty)):
    return apply_feedback(db, request.query_id, request.faculty_name, request.domain, request.feedback)


# ══════════════════════════════════════════════════════════════════════════════
#  ACTIVE CHAT — Request Management
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/chat/request")
def create_chat_request(request: ChatRequestIn, db: Session = Depends(get_db),
                        user: dict = Depends(require_student)):
    expire_old_requests(db)
    student_email = user.get("sub")

    # Rate limit: max pending requests
    pending = db.query(ChatRequest).filter(
        ChatRequest.student_email == student_email,
        ChatRequest.status == "pending"
    ).count()
    if pending >= MAX_PENDING_REQUESTS:
        raise HTTPException(status_code=429,
            detail=f"You can only have {MAX_PENDING_REQUESTS} pending chat requests at a time.")

    # No duplicate pending/accepted with same faculty
    existing = db.query(ChatRequest).filter(
        ChatRequest.student_email == student_email,
        ChatRequest.faculty_name == request.faculty_name,
        ChatRequest.status.in_(["pending", "accepted"])
    ).first()
    if existing:
        raise HTTPException(status_code=400,
            detail=f"You already have a pending or active request with {request.faculty_name}.")

    # No active session with same faculty
    active = db.query(ChatSession).filter(
        ChatSession.student_email == student_email,
        ChatSession.faculty_name == request.faculty_name,
        ChatSession.status == "active"
    ).first()
    if active:
        raise HTTPException(status_code=400,
            detail=f"You already have an active chat session with {request.faculty_name}.")

    # Derive topic from query if not provided
    topic = request.topic
    if not topic and request.query_id:
        q = db.query(QueryModel).filter(QueryModel.id == request.query_id).first()
        if q:
            topic = q.refined_query or q.original_query

    chat_req = ChatRequest(
        student_email=student_email,
        faculty_name=request.faculty_name,
        query_id=request.query_id,
        topic=topic,
        expires_at=datetime.utcnow() + timedelta(minutes=CHAT_REQUEST_EXPIRY_MIN)
    )
    db.add(chat_req)
    db.commit()
    db.refresh(chat_req)

    return {
        "request_id": chat_req.id,
        "status":     "pending",
        "expires_at": chat_req.expires_at.isoformat(),
        "message":    f"Chat request sent to {request.faculty_name}. Expires in {CHAT_REQUEST_EXPIRY_MIN} min."
    }


@router.get("/chat/requests/incoming")
def get_incoming_requests(db: Session = Depends(get_db),
                          user: dict = Depends(require_faculty)):
    expire_old_requests(db)
    reqs = db.query(ChatRequest).filter(
        ChatRequest.faculty_name == user.get("name"),
        ChatRequest.status == "pending"
    ).order_by(ChatRequest.created_at.desc()).all()

    result = []
    for r in reqs:
        student = db.query(User).filter(User.email == r.student_email).first()
        mins_left = max(0, int((r.expires_at - datetime.utcnow()).total_seconds() / 60))
        result.append({
            "request_id":   r.id,
            "student_email": r.student_email,
            "student_name": student.name if student else r.student_email,
            "topic":        r.topic,
            "query_id":     r.query_id,
            "status":       r.status,
            "mins_left":    mins_left,
            "created_at":   r.created_at.isoformat()
        })
    return result


@router.get("/chat/requests/outgoing")
def get_outgoing_requests(db: Session = Depends(get_db),
                          user: dict = Depends(require_student)):
    expire_old_requests(db)
    reqs = db.query(ChatRequest).filter(
        ChatRequest.student_email == user.get("sub")
    ).order_by(ChatRequest.created_at.desc()).limit(20).all()

    return [{
        "request_id": r.id,
        "faculty_name": r.faculty_name,
        "topic":      r.topic,
        "query_id":   r.query_id,
        "status":     r.status,
        "created_at": r.created_at.isoformat(),
        "expires_at": r.expires_at.isoformat()
    } for r in reqs]


@router.post("/chat/request/{request_id}/accept")
def accept_chat_request(request_id: int, db: Session = Depends(get_db),
                        user: dict = Depends(require_faculty)):
    expire_old_requests(db)
    req = db.query(ChatRequest).filter(ChatRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.faculty_name != user.get("name"):
        raise HTTPException(status_code=403, detail="Not your request")
    if req.status != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already {req.status}")

    req.status = "accepted"
    session = ChatSession(
        student_email=req.student_email,
        faculty_name=req.faculty_name,
        topic=req.topic
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    sys_msg = ChatMessage(
        session_id=session.id,
        sender_email="system",
        sender_name="System",
        sender_role="system",
        content=f"Chat session started. Topic: {req.topic or 'General discussion'}"
    )
    db.add(sys_msg)

    # Auto-post the student's confirmed query as their first message
    if req.topic:
        student = db.query(User).filter(User.email == req.student_email).first()
        student_name = student.name if student else req.student_email
        student_intro = ChatMessage(
            session_id=session.id,
            sender_email=req.student_email,
            sender_name=student_name,
            sender_role="student",
            content=req.topic
        )
        db.add(student_intro)

    db.commit()

    return {
        "session_id":    session.id,
        "student_email": req.student_email,
        "topic":         req.topic,
        "message":       "Chat request accepted. Session is now active."
    }


@router.post("/chat/request/{request_id}/decline")
def decline_chat_request(request_id: int, db: Session = Depends(get_db),
                          user: dict = Depends(require_faculty)):
    req = db.query(ChatRequest).filter(ChatRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    if req.faculty_name != user.get("name"):
        raise HTTPException(status_code=403, detail="Not your request")
    if req.status != "pending":
        raise HTTPException(status_code=400, detail=f"Request is already {req.status}")

    req.status = "declined"
    db.commit()
    return {"message": "Request declined."}


# ══════════════════════════════════════════════════════════════════════════════
#  ACTIVE CHAT — Messaging
# ══════════════════════════════════════════════════════════════════════════════

@router.post("/chat/message")
def send_message(request: SendMessageIn, db: Session = Depends(get_db),
                 user: dict = Depends(get_current_user)):
    session = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Session is closed")

    user_email = user.get("sub")
    user_role  = user.get("role")
    user_name  = user.get("name")

    if user_role == "student" and session.student_email != user_email:
        raise HTTPException(status_code=403, detail="Not your session")
    if user_role == "faculty" and session.faculty_name != user_name:
        raise HTTPException(status_code=403, detail="Not your session")

    msg = ChatMessage(
        session_id=request.session_id,
        sender_email=user_email,
        sender_name=user_name,
        sender_role=user_role,
        content=request.content
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    return {
        "message_id":  msg.id,
        "session_id":  msg.session_id,
        "sender_name": msg.sender_name,
        "sender_role": msg.sender_role,
        "content":     msg.content,
        "timestamp":   msg.timestamp.isoformat()
    }


@router.get("/chat/session/{session_id}/messages")
def get_session_messages(session_id: int, db: Session = Depends(get_db),
                          user: dict = Depends(get_current_user)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_email = user.get("sub")
    user_role  = user.get("role")
    user_name  = user.get("name")

    if user_role == "student" and session.student_email != user_email:
        raise HTTPException(status_code=403, detail="Not your session")
    if user_role == "faculty" and session.faculty_name != user_name:
        raise HTTPException(status_code=403, detail="Not your session")

    messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.timestamp).all()

    other_party = session.faculty_name if user_role == "student" else session.student_email

    return {
        "session_id":  session_id,
        "status":      session.status,
        "topic":       session.topic,
        "other_party": other_party,
        "messages": [{
            "id":          m.id,
            "sender_name": m.sender_name,
            "sender_role": m.sender_role,
            "content":     m.content,
            "timestamp":   m.timestamp.isoformat()
        } for m in messages]
    }


@router.get("/chat/sessions")
def get_user_sessions(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    user_email = user.get("sub")
    user_role  = user.get("role")
    user_name  = user.get("name")

    if user_role == "student":
        sessions = db.query(ChatSession).filter(
            ChatSession.student_email == user_email
        ).order_by(ChatSession.created_at.desc()).all()
    else:
        sessions = db.query(ChatSession).filter(
            ChatSession.faculty_name == user_name
        ).order_by(ChatSession.created_at.desc()).all()

    result = []
    for s in sessions:
        last_msg = db.query(ChatMessage).filter(
            ChatMessage.session_id == s.id,
            ChatMessage.sender_role != "system"
        ).order_by(ChatMessage.timestamp.desc()).first()

        other = s.faculty_name if user_role == "student" else s.student_email
        result.append({
            "session_id":        s.id,
            "status":            s.status,
            "topic":             s.topic,
            "other_party":       other,
            "created_at":        s.created_at.isoformat(),
            "last_message":      (last_msg.content[:60] + "…") if last_msg and len(last_msg.content) > 60 else (last_msg.content if last_msg else "Session started"),
            "last_message_time": last_msg.timestamp.isoformat() if last_msg else s.created_at.isoformat()
        })
    return result


@router.post("/chat/session/{session_id}/close")
def close_session(session_id: int, db: Session = Depends(get_db),
                  user: dict = Depends(get_current_user)):
    session = db.query(ChatSession).filter(ChatSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    user_role = user.get("role")
    if user_role == "student" and session.student_email != user.get("sub"):
        raise HTTPException(status_code=403, detail="Not your session")
    if user_role == "faculty" and session.faculty_name != user.get("name"):
        raise HTTPException(status_code=403, detail="Not your session")

    session.status = "closed"

    closing_msg = ChatMessage(
        session_id=session_id,
        sender_email="system",
        sender_name="System",
        sender_role="system",
        content=f"Chat session closed by {user.get('name')}."
    )
    db.add(closing_msg)
    db.commit()
    return {"message": "Session closed."}
