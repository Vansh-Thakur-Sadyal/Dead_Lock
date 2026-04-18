from app.utils.constants import SEMANTIC_WEIGHT, DOMAIN_WEIGHT, DEFAULT_DOMAIN_SCORE
from app.utils.helpers import clamp

def compute_final_score(sim_score: float, domain_score: float) -> float:
    return clamp((SEMANTIC_WEIGHT * sim_score) + (DOMAIN_WEIGHT * domain_score))