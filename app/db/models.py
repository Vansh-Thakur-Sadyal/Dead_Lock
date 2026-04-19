from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    domains = Column(JSON)
    projects = Column(JSON)
    papers = Column(JSON)
    domain_scores = Column(JSON)
    active_queries = Column(Integer, default=0)


class Query(Base):
    __tablename__ = "queries"
    id = Column(Integer, primary_key=True, index=True)
    original_query = Column(Text)
    refined_query = Column(Text, nullable=True)
    domain = Column(String, nullable=True)
    level = Column(String, nullable=True)
    assigned_faculty = Column(String, nullable=True)
    status = Column(String, default="pending")
    attempt = Column(Integer, default=1)
    escalation_level = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    student_email = Column(String, nullable=True)
    response_time = Column(Float, nullable=True)
    rating = Column(String, nullable=True)
    faculty_response = Column(Text, nullable=True)
    research_papers = Column(JSON, nullable=True)  # [{title, link, summary}]


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer)
    faculty_name = Column(String)
    feedback = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatRequest(Base):
    __tablename__ = "chat_requests"
    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String)
    faculty_name = Column(String)
    query_id = Column(Integer, nullable=True)
    topic = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending/accepted/declined/expired
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)


class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    student_email = Column(String)
    faculty_name = Column(String)
    topic = Column(String, nullable=True)
    status = Column(String, default="active")  # active/closed
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer)
    sender_email = Column(String)
    sender_name = Column(String)
    sender_role = Column(String)  # student/faculty/system
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
