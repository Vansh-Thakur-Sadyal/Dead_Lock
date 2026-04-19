import httpx
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def fetch_arxiv_papers(query: str, max_results: int = 3) -> list:
    url = "https://export.arxiv.org/api/query"  # fixed: https not http
    params = {"search_query": f"all:{query}", "start": 0, "max_results": max_results}
    try:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(url, params=params)
        return parse_arxiv(response.text)
    except Exception as e:
        logger.error(f"arXiv fetch failed: {e}")
        return []

def parse_arxiv(xml_text: str) -> list:
    import xml.etree.ElementTree as ET
    ns = "{http://www.w3.org/2005/Atom}"
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    papers = []
    for entry in root.findall(f"{ns}entry"):
        t = entry.find(f"{ns}title")
        s = entry.find(f"{ns}summary")
        i = entry.find(f"{ns}id")
        if t is None or i is None:
            continue
        papers.append({
            "title":   t.text.strip().replace("\n", " "),
            "summary": (s.text.strip()[:200] + "…") if s is not None else "",
            "link":    i.text.strip()
        })
    return papers