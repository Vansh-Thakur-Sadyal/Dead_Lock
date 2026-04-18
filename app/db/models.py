from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    domains = Column(JSON)           # ["machine learning", "cloud"]
    projects = Column(JSON)          # ["Traffic prediction..."]
    papers = Column(JSON)            # ["Deep Learning for Traffic"]
    domain_scores = Column(JSON)     # {"machine learning": 0.9}
    active_queries = Column(Integer, default=0)


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    original_query = Column(Text)
    refined_query = Column(Text, nullable=True)
    domain = Column(String, nullable=True)
    level = Column(String, nullable=True)
    assigned_faculty = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending/routed/escalated/resolved
    attempt = Column(Integer, default=1)
    escalation_level = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response_time = Column(Float, nullable=True)
    rating = Column(String, nullable=True)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer)
    faculty_name = Column(String)
    feedback = Column(String)       # "relevant" / "irrelevant"
    timestamp = Column(DateTime, default=datetime.utcnow)