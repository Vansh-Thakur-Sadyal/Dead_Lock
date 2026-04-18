from fastapi import FastAPI
from app.api import chat, faculty, health
from app.db.database import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Faculty Matching System")

app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(faculty.router, tags=["Faculty"])