def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    return max(min_val, min(max_val, value))

def normalize_feedback_score(relevant: int, irrelevant: int) -> float:
    total = relevant + irrelevant
    if total == 0:
        return 0.5
    return clamp((relevant - irrelevant) / total)

def get_availability_score(active_queries: int) -> float:
    return 1 / (1 + active_queries)

def normalize_domain(domain: str) -> str:
    domain = domain.lower().strip()

    mapping = {
    # --- AI / ML ---
    "ai": "machine learning",
    "artificial intelligence": "machine learning",
    "ml": "machine learning",
    "machine learning": "machine learning",
    "predictive modeling": "machine learning",
    "prediction": "machine learning",
    "regression": "machine learning",
    "classification": "machine learning",

    # --- Deep Learning ---
    "deep learning": "deep learning",
    "dl": "deep learning",
    "neural network": "deep learning",
    "cnn": "deep learning",
    "rnn": "deep learning",
    "lstm": "deep learning",
    "transformer": "deep learning",

    # --- NLP ---
    "nlp": "natural language processing",
    "natural language": "natural language processing",
    "text processing": "natural language processing",
    "chatbot": "natural language processing",
    "language model": "natural language processing",
    "text analysis": "natural language processing",
    "sentiment analysis": "natural language processing",

    # --- Computer Vision ---
    "cv": "computer vision",
    "computer vision": "computer vision",
    "image processing": "computer vision",
    "object detection": "computer vision",
    "image classification": "computer vision",
    "video analysis": "computer vision",

    # --- Data Science / Stats ---
    "data science": "data science",
    "data analysis": "data science",
    "analytics": "data science",
    "big data": "data science",
    "statistics": "statistics",
    "statistical analysis": "statistics",
    "probability": "statistics",

    # --- Cloud ---
    "cloud": "cloud computing",
    "aws": "cloud computing",
    "azure": "cloud computing",
    "gcp": "cloud computing",
    "cloud computing": "cloud computing",
    "serverless": "cloud computing",

    # --- Distributed ---
    "distributed": "distributed systems",
    "distributed systems": "distributed systems",
    "microservices": "distributed systems",
    "scalable systems": "distributed systems",

    # --- Security ---
    "cybersecurity": "cybersecurity",
    "security": "cybersecurity",
    "network security": "network security",
    "encryption": "network security",
    "intrusion": "cybersecurity",
    "hacking": "cybersecurity",

    # --- IoT ---
    "iot": "internet of things",
    "internet of things": "internet of things",
    "sensor": "internet of things",
    "smart devices": "internet of things",

    # --- Embedded ---
    "embedded": "embedded systems",
    "embedded systems": "embedded systems",
    "microcontroller": "embedded systems",

    # --- Blockchain ---
    "blockchain": "blockchain",
    "crypto": "blockchain",
    "smart contract": "blockchain",
    "web3": "blockchain",

    # --- Robotics ---
    "robotics": "robotics",
    "robot": "robotics",
}

    return mapping.get(domain, domain)

def detect_domain_from_text(text: str) -> str | None:
    text = text.lower()

    known_domains = [
        "machine learning",
        "deep learning",
        "natural language processing",
        "computer vision",
        "data science",
        "statistics",
        "cloud computing",
        "distributed systems",
        "cybersecurity",
        "network security",
        "internet of things",
        "embedded systems",
        "blockchain",
        "robotics"
    ]

    for d in known_domains:
        if d in text:
            return d

    return None