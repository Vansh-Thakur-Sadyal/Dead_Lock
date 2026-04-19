from sqlalchemy.orm import Session
from app.core.chatbot.query_processor import process_query
from app.core.chatbot.rag_controller import get_papers
from app.core.chatbot.response_builder import build_response
from app.core.matcher import match_faculty
from app.db.crud import create_query

async def handle_query(raw_query: str, db: Session, student_email: str) -> dict:
    processed = process_query(raw_query)
    refined = processed.get("refined_query", raw_query)
    domain = processed.get("domain", "general")
    level = processed.get("level", "unknown")

    query_record = create_query(db, original=raw_query, refined=refined, domain=domain, level=level, student_email=student_email)

    matches = match_faculty(db, refined, domain)
    papers = await get_papers(refined)

    return {
        "query_id": query_record.id,
        **build_response(refined, matches, papers)
    }