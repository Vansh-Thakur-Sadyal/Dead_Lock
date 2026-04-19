from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import User, Faculty
from app.utils.constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta

router = APIRouter()

# --- Schemas ---
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str  # "student" or "faculty"

class LoginRequest(BaseModel):
    email: str
    password: str

# --- Helpers ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

def create_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

# --- Routes ---
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(User).filter(User.email == request.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # If faculty, email must match faculty record
    if request.role == "faculty":
        faculty = db.query(Faculty).filter(Faculty.email == request.email).first()
        if not faculty:
            raise HTTPException(status_code=400, detail="Email not found in faculty records")

    user = User(
        name=request.name,
        email=request.email,
        hashed_password=hash_password(request.password),
        role=request.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token({"sub": user.email, "role": user.role, "name": user.name})
    return {"access_token": token, "role": user.role, "name": user.name}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.email, "role": user.role, "name": user.name})
    return {"access_token": token, "role": user.role, "name": user.name}