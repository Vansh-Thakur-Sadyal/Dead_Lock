from sqlalchemy.orm import Session
from app.core.chatbot.query_processor import process_query
from app.core.chatbot.rag_controller import get_papers
from app.core.matcher import match_faculty
from app.db.crud import create_query
from app.utils.helpers import normalize_domain, detect_domain_from_text


async def handle_query(raw_query: str, db: Session) -> dict:
    # Step 1: Refine query
    processed = process_query(raw_query)
    refined = processed.get("refined_query", raw_query)
    level = processed.get("level", "unknown")

    # 🔥 Step 2: Domain logic (FIXED)

    # 1. Try direct detection from user input
    domain = detect_domain_from_text(raw_query)

    # 2. If not found → use LLM output
    if not domain:
        domain = normalize_domain(processed.get("domain", "general"))

    # 3. If still weak → fallback to refined query
    if domain in ["general", "unknown", ""]:
        domain = normalize_domain(refined)

    # Step 3: Save to DB
    query_record = create_query(
        db,
        original=raw_query,
        refined=refined,
        domain=domain,
        level=level
    )

    # Step 4: Match faculty
    matches = match_faculty(db, refined, domain)

    # Step 5: Fetch papers
    papers = await get_papers(refined)

    # Step 6: Build response
    return {
        "query_id": query_record.id,
        "refined_query": refined,
        "domain": domain,
        "level": level,
        "faculty_recommendations": matches,
        "research_papers": papers
    }