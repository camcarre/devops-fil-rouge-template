import os

# Doit être défini avant l'import de src.db.database et src.security (lecture au niveau module).
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import src.models  # noqa: F401  enregistre les tables sur Base.metadata
from src.db.database import Base, get_db
from src.main import app


@pytest.fixture
def db_engine():
    """SQLite en mémoire, partagé sur une connexion unique le temps du test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_engine):
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_token(client):
    """Enregistre un utilisateur et renvoie un JWT valide (auth réelle, pas de mock)."""
    client.post(
        "/auth/register",
        json={"username": "tester", "email": "tester@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/auth/login",
        data={"username": "tester@example.com", "password": "secret123"},
    )
    return resp.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
