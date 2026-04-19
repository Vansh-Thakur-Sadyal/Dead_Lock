faculty_data = [
    {
        "name": "Dr. Sharma",
        "email": "sharma@university.edu",
        "domains": ["machine learning", "deep learning", "computer vision"],
        "projects": [
            "Developed a machine learning model to predict traffic flow and congestion using historical time-series data and real-time sensor inputs.",
            "Built an image classification system using convolutional neural networks for medical image analysis."
        ],
        "papers": [
            "Research on deep learning techniques for traffic forecasting and intelligent transportation systems.",
            "Study of CNN architectures for accurate medical image classification and detection."
        ],
        "domain_scores": {"machine learning": 0.95, "deep learning": 0.9, "computer vision": 0.85},
        "active_queries": 0
    },
    {
        "name": "Dr. Verma",
        "email": "verma@university.edu",
        "domains": ["natural language processing", "machine learning"],
        "projects": [
            "Built a sentiment analysis system using transformer-based NLP models for student feedback analysis.",
            "Developed an AI chatbot for answering academic queries using natural language understanding."
        ],
        "papers": [
            "Survey on transformer models and their applications in natural language processing.",
            "Research on NLP techniques for analyzing student feedback and educational data."
        ],
        "domain_scores": {"natural language processing": 0.9, "machine learning": 0.75},
        "active_queries": 0
    },
    {
        "name": "Dr. Patel",
        "email": "patel@university.edu",
        "domains": ["cloud computing", "distributed systems"],
        "projects": [
            "Designed a Kubernetes-based autoscaling system for handling dynamic cloud workloads efficiently.",
            "Implemented a multi-cloud deployment architecture for scalable distributed applications."
        ],
        "papers": [
            "Research on cloud cost optimization strategies in large-scale distributed systems.",
            "Study of serverless computing architectures and performance optimization."
        ],
        "domain_scores": {"cloud computing": 0.92, "distributed systems": 0.88},
        "active_queries": 0
    },
    {
        "name": "Dr. Rao",
        "email": "rao@university.edu",
        "domains": ["cybersecurity", "network security"],
        "projects": [
            "Developed an intrusion detection system using machine learning for identifying network attacks.",
            "Built a secure file sharing system with encryption and authentication mechanisms."
        ],
        "papers": [
            "Research on machine learning techniques for intrusion detection in network security.",
            "Study of zero trust security models for modern network architectures."
        ],
        "domain_scores": {"cybersecurity": 0.9, "network security": 0.85},
        "active_queries": 0
    },
    {
        "name": "Dr. Gupta",
        "email": "gupta@university.edu",
        "domains": ["data science", "machine learning", "statistics"],
        "projects": [
            "Built a predictive analytics model to analyze student performance using statistical learning techniques.",
            "Developed a fraud detection system using machine learning models on financial transaction data."
        ],
        "papers": [
            "Research on statistical learning methods for predictive analytics in education.",
            "Study of machine learning approaches for fraud detection in financial systems."
        ],
        "domain_scores": {"data science": 0.92, "machine learning": 0.8, "statistics": 0.9},
        "active_queries": 0
    },
    {
        "name": "Dr. Singh",
        "email": "singh@university.edu",
        "domains": ["internet of things", "embedded systems"],
        "projects": [
            "Designed a smart campus system using IoT sensors for monitoring and automation.",
            "Built an IoT-based sensor network for real-time environmental data collection."
        ],
        "papers": [
            "Research on IoT applications in smart cities and intelligent infrastructure.",
            "Study of edge computing techniques for efficient IoT data processing."
        ],
        "domain_scores": {"internet of things": 0.91, "embedded systems": 0.8},
        "active_queries": 0
    },
    {
        "name": "Dr. Mehta",
        "email": "mehta@university.edu",
        "domains": ["blockchain", "distributed systems"],
        "projects": [
            "Developed a decentralized voting system using blockchain for secure and transparent elections.",
            "Built a blockchain-based supply chain tracking system for ensuring data integrity."
        ],
        "papers": [
            "Research on blockchain applications in healthcare data management.",
            "Study of smart contract security and decentralized applications."
        ],
        "domain_scores": {"blockchain": 0.88, "distributed systems": 0.8},
        "active_queries": 0
    },
    {
        "name": "Dr. Khan",
        "email": "khan@university.edu",
        "domains": ["computer vision", "robotics"],
        "projects": [
            "Developed an object detection system using YOLO for real-time visual recognition.",
            "Built an autonomous robot navigation system using computer vision techniques."
        ],
        "papers": [
            "Research on real-time object detection using deep learning models.",
            "Study of robot vision systems for autonomous navigation."
        ],
        "domain_scores": {"computer vision": 0.9, "robotics": 0.85},
        "active_queries": 0
    }
]

if __name__ == "__main__":
    import json
    print(json.dumps(faculty_data, indent=2))
    print(f"\n✅ Generated {len(faculty_data)} faculty records.")

student_data = [
    {
        "name": "Rahul Sharma",
        "email": "rahul@student.edu",
        "password": "password123",
        "role": "student"
    },
    {
        "name": "Priya Singh",
        "email": "priya@student.edu",
        "password": "password123",
        "role": "student"
    },
    {
        "name": "Aryan Mehta",
        "email": "aryan@student.edu",
        "password": "password123",
        "role": "student"
    }
]

sample_queries = [
    {
        "original_query": "I want to do a machine learning project",
        "refined_query": "Beginner level machine learning project using Python",
        "domain": "machine learning",
        "level": "beginner",
        "student_email": "rahul@student.edu",
        "assigned_faculty": "Dr. Sharma",
        "status": "routed"
    },
    {
        "original_query": "Help me with NLP research",
        "refined_query": "Natural language processing research guidance for intermediate level",
        "domain": "natural language processing",
        "level": "intermediate",
        "student_email": "priya@student.edu",
        "assigned_faculty": "Dr. Verma",
        "status": "routed"
    },
    {
        "original_query": "I need help with cloud deployment",
        "refined_query": "Cloud deployment and DevOps guidance for beginners",
        "domain": "cloud computing",
        "level": "beginner",
        "student_email": "aryan@student.edu",
        "assigned_faculty": "Dr. Patel",
        "status": "resolved",
        "faculty_response": "I can help you with cloud deployment. Start with AWS EC2 basics."
    },
    {
        "original_query": "Cybersecurity project ideas",
        "refined_query": "Advanced cybersecurity project ideas and implementation guidance",
        "domain": "cybersecurity",
        "level": "advanced",
        "student_email": "rahul@student.edu",
        "assigned_faculty": None,
        "status": "pending"
    }
]