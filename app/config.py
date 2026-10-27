import os

from dotenv import load_dotenv

load_dotenv()

# SQLite works out of the box; set DATABASE_URL in .env to use MySQL instead.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./splitkaro.db")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
