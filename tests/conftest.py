import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    """A test client backed by a fresh in-memory SQLite database for every test."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # Not used as a context manager, so the app's startup doesn't touch the real database.
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def make_user(client):
    """Registers a user and returns (user_id, auth_headers)."""

    def _make_user(name: str, email: str, password: str = "password123"):
        res = client.post("/auth/register", json={"name": name, "email": email, "password": password})
        assert res.status_code == 201, res.text
        token = client.post("/auth/login", data={"username": email, "password": password}).json()
        return res.json()["id"], {"Authorization": f"Bearer {token['access_token']}"}

    return _make_user
