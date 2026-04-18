import httpx
import json
from app.utils.logger import get_logger

logger = get_logger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def query_ollama(prompt: str) -> str:
    try:
        response = httpx.post(
            OLLAMA_URL,
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        return response.json().get("response", "").strip()
    except Exception as e:
        logger.error(f"Ollama call failed: {e}")
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