from sqlalchemy.orm import Session
from app.services.embeddings import get_embedding, get_similarity, build_faculty_text
from app.services.faculty_service import get_faculty_list
from app.core.scoring import compute_final_score
from app.utils.constants import DEFAULT_DOMAIN_SCORE
from app.services.llm import generate_explanation

def match_faculty(db: Session, refined_query: str, domain: str, top_k: int = 3) -> list:
    query_vec = get_embedding(refined_query)
    faculty_list = get_faculty_list(db)
    results = []

    for faculty in faculty_list:
        faculty_text = build_faculty_text(faculty)
        faculty_vec = get_embedding(faculty_text)
        sim_score = get_similarity(query_vec, faculty_vec)
        domain_score = (faculty.domain_scores or {}).get(domain, DEFAULT_DOMAIN_SCORE)
        if domain in (faculty.domains or []):
            domain_score += 0.05
        final_score = compute_final_score(sim_score, domain_score)
        explanation = generate_explanation(faculty.name, domain, sim_score, domain_score)

        results.append({
            "faculty_name": faculty.name,
            "email": faculty.email,
            "sim_score": round(sim_score, 4),
            "domain_score": round(domain_score, 4),
            "final_score": round(final_score, 4),
            "explanation": explanation
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)
    return results[:top_k]