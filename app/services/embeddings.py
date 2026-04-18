from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> np.ndarray:
    return model.encode(text, convert_to_numpy=True)

def get_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return float(cosine_similarity([vec1], [vec2])[0][0])

def build_faculty_text(faculty) -> str:
    domains = ", ".join(faculty.domains or [])
    projects = ". ".join(faculty.projects or [])
    papers = ". ".join(faculty.papers or [])

    return f"""
    Faculty expertise in {domains}.
    Worked on projects like {projects}.
    Published research including {papers}.
    """