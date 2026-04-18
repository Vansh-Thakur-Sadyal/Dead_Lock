import httpx
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def fetch_arxiv_papers(query: str, max_results: int = 3) -> list:
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=10)
        entries = parse_arxiv(response.text)
        return entries
    except Exception as e:
        logger.error(f"arXiv fetch failed: {e}")
        return []

def parse_arxiv(xml_text: str) -> list:
    import xml.etree.ElementTree as ET
    ns = "{http://www.w3.org/2005/Atom}"
    root = ET.fromstring(xml_text)
    papers = []
    for entry in root.findall(f"{ns}entry"):
        papers.append({
            "title": entry.find(f"{ns}title").text.strip(),
            "summary": entry.find(f"{ns}summary").text.strip()[:200],
            "link": entry.find(f"{ns}id").text.strip()
        })
    return papers