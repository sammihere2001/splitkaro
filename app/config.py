import os

from dotenv import load_dotenv

load_dotenv()


def normalize_database_url(url: str) -> str:
    """Hosting providers hand out "postgres://..." or "postgresql://..." URLs.
    SQLAlchemy needs "postgresql+psycopg://..." to know which driver (psycopg 3) to use."""
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


# SQLite works out of the box; set DATABASE_URL in .env to use MySQL or PostgreSQL instead.
DATABASE_URL = normalize_database_url(os.getenv("DATABASE_URL", "sqlite:///./splitkaro.db"))

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
