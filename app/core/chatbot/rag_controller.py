from app.services.papers import fetch_arxiv_papers

async def get_papers(query: str) -> list:
    return await fetch_arxiv_papers(query)