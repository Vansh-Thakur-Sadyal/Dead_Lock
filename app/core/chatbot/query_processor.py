from app.services.llm import refine_query

def process_query(raw_query: str) -> dict:
    return refine_query(raw_query)