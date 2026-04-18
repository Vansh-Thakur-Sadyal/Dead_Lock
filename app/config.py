from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    APP_ENV: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./faculty_system.db"
    OPENAI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()