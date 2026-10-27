import pytest

from app.config import normalize_database_url


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("postgres://u:p@host/db", "postgresql+psycopg://u:p@host/db"),
        ("postgresql://u:p@host/db?sslmode=require", "postgresql+psycopg://u:p@host/db?sslmode=require"),
        ("postgresql+psycopg://u:p@host/db", "postgresql+psycopg://u:p@host/db"),
        ("mysql+pymysql://u:p@host/db", "mysql+pymysql://u:p@host/db"),
        ("sqlite:///./splitkaro.db", "sqlite:///./splitkaro.db"),
    ],
)
def test_normalize_database_url(url, expected):
    assert normalize_database_url(url) == expected
