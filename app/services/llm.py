import httpx
import json
from app.utils.logger import get_logger

logger = get_logger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def query_ollama(prompt: str) -> str:
    """Synchronous Ollama call — only use from sync contexts (e.g. generate_explanation)."""
    try:
        response = httpx.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=90
        )
        return response.json().get("response", "").strip()
    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
        return ""

async def query_ollama_async(prompt: str) -> str:
    """Non-blocking async Ollama call — use from async FastAPI endpoints."""
    try:
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": prompt, "stream": False}
            )
            return response.json().get("response", "").strip()
    except Exception as e:
        logger.error(f"Ollama async call failed: {e}")
        return ""

def refine_query(raw_query: str) -> dict:
    prompt = f"""
You are an academic assistant.

A student query: "{raw_query}"

Your job:
- DO NOT ask questions
- DO NOT request clarification
- ALWAYS rewrite the query into a clear, specific academic query
- Refined query must be ONE sentence only, max 15 words

Also extract:
- domain (machine learning, NLP, cloud, etc.)
- level (beginner/intermediate/advanced)

Respond ONLY in valid JSON:
{{
  "is_vague": true,
  "refined_query": "specific improved query",
  "domain": "one domain only",
  "level": "beginner/intermediate/advanced"
}}
"""
    raw = query_ollama(prompt)
    try:
        return json.loads(raw)
    except:
        logger.error(f"Failed to parse LLM response: {raw}")
        return {
            "is_vague": False,
            "refined_query": raw_query,
            "domain": "general",
            "level": "unknown"
        }

async def conversational_chat(message: str, history: list = []) -> dict:
    """Phase 1: Detect vague queries, ask clarifying questions or suggest research directions."""
    history_text = ""
    if history:
        lines = []
        for h in history[-8:]:  # last 8 turns for context
            role = "Student" if h.get("role") == "user" else "AI"
            lines.append(f"{role}: {h.get('content', '')}")
        history_text = "\nConversation so far:\n" + "\n".join(lines) + "\n"

    prompt = f"""You are an AI academic advisor helping students find the right faculty mentor.
{history_text}
Latest student message: "{message}"

Instructions:
1. Read the full conversation above to understand context before responding.
2. If the overall research topic is still vague or unclear, ask 1 short clarifying question (under 60 words).
3. If the topic is now specific enough (domain + interest clear), summarize it briefly and set is_vague to false.
4. Never repeat questions already asked. Build on what the student said.
5. Be encouraging and academic in tone.

Reply ONLY in valid JSON (no extra text):
{{
  "reply": "your response here",
  "is_vague": true or false,
  "topic_hint": "2-4 word topic summary"
}}"""
    raw = await query_ollama_async(prompt)
    try:
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except Exception:
        return {
            "reply": "Interesting! Could you tell me a bit more about what specific aspect you want to explore and what level you're at — beginner project, thesis, or advanced research?",
            "is_vague": True,
            "topic_hint": "research query"
        }


async def extract_query_details(message: str) -> dict:
    """Phase 2: Extract refined_query, domain, level from confirmed student query."""
    prompt = f"""Extract structured academic info from this student query: "{message}"

Reply ONLY in valid JSON:
{{
  "refined_query": "clear one-sentence academic version of the query, max 20 words",
  "domain": "one of: machine learning, deep learning, natural language processing, computer vision, data science, cloud computing, cybersecurity, blockchain, internet of things, robotics, distributed systems, statistics, general",
  "level": "one of: beginner, intermediate, advanced"
}}"""
    raw = await query_ollama_async(prompt)
    try:
        start = raw.find("{")
        end   = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except Exception:
        return {"refined_query": message, "domain": "general", "level": "intermediate"}


def generate_explanation(faculty_name: str, domain: str, sim_score: float, domain_score: float) -> str:
    prompt = f"""Write one sentence (max 20 words) explaining why {faculty_name} is recommended for a {domain} query.
Only mention: their domain expertise and match score.
Do NOT mention medical, healthcare, or anything not related to {domain}.
Output only the sentence, nothing else."""

    result = query_ollama(prompt)
    if not result:
        return f"{faculty_name} is recommended for strong expertise in {domain} with a match score of {sim_score:.2f}."
    
    # Fallback if response is too long
    if len(result.split()) > 25:
        return f"{faculty_name} is recommended for strong expertise in {domain} with a match score of {sim_score:.2f}."
    
    return result