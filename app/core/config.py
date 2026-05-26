import os
from dotenv import load_dotenv

# Load env variables from .env if present
load_dotenv()

class Settings:
    PROJECT_NAME: str = "Student Nexus API"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "9e3c98341620a2e7c4f4b23d9178e242cd1a403075c3db89d53c7a0c1bf6a3b2")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # DB configuration. Default is an async sqlite database.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./nexus.db")

settings = Settings()
