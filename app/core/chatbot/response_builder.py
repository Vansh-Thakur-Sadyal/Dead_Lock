def build_response(refined_query: str, faculty_matches: list, papers: list) -> dict:
    return {
        "refined_query": refined_query,
        "faculty_recommendations": faculty_matches,
        "research_papers": papers
    }