from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, faculty, health, auth, student
from app.db.database import engine
from app.db.models import Base
import sqlalchemy as sa

Base.metadata.create_all(bind=engine)

# ── Column migrations for existing databases ──
def _run_migrations():
    _cols = [
        ("queries",        "research_papers", "JSON"),
        ("chat_requests",  "id",              None),   # just checks table exists
        ("chat_sessions",  "id",              None),
        ("chat_messages",  "id",              None),
    ]
    with engine.connect() as conn:
        existing = sa.inspect(engine).get_table_names()
        for table, col, coltype in _cols:
            if col == "id" or table not in existing:
                continue
            existing_cols = [c["name"] for c in sa.inspect(engine).get_columns(table)]
            if col not in existing_cols:
                conn.execute(sa.text(f"ALTER TABLE {table} ADD COLUMN {col} {coltype}"))
                conn.commit()

_run_migrations()

app = FastAPI(title="AI Faculty Matching System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(faculty.router, tags=["Faculty"])
app.include_router(student.router, tags=["Student"])