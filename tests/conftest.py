import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def headers(client):
    client.post(
        "/auth/register",
        json={"username": "rifayet", "email": "rifayet@mail.com", "password": "123456"},
    )
    response = client.post(
        "/auth/login", json={"username": "rifayet", "password": "123456"}
    )
    token = response.json()["access_token"]
    return {"Authorization": "Bearer " + token}


@pytest.fixture
def transaction(client, headers):
    response = client.post(
        "/transactions",
        headers=headers,
        json={
            "title": "Lunch",
            "amount": 250,
            "type": "expense",
            "category": "Food",
            "date": "2025-01-10",
        },
    )
    return response.json()
