import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from main import app, get_db

@pytest.fixture(scope="module")
def db_engine():
    """Start a temporary Postgres container and provide SQLAlchemy engine."""
    with PostgresContainer("postgres:15-alpine") as postgres:

        engine = create_engine(postgres.get_connection_url())
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    username VARCHAR UNIQUE NOT NULL,
                    email VARCHAR UNIQUE NOT NULL,
                    hashed_password VARCHAR NOT NULL,
                    role VARCHAR NOT NULL DEFAULT 'user'
                );
            """))
            conn.commit()
        yield engine
        engine.dispose()


@pytest.fixture()
def client(db_engine):
    """Override get_db before creating TestClient."""
    SessionLocal = sessionmaker(bind=db_engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides.clear()
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_create_user_success(client):
    response = client.post(
        "/signup",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["role"] == "user"
    assert "id" in data


def test_create_user_duplicate_email(client):
    client.post(
        "/signup",
        json={"username": "user1", "email": "dup@example.com", "password": "password123"},
    )
    response = client.post(
        "/signup",
        json={"username": "user2", "email": "dup@example.com", "password": "password456"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already register"}


def test_login_success(client):
    client.post(
        "/signup",
        json={"username": "loginuser", "email": "login@example.com", "password": "password123"},
    )
    response = client.post(
        "/token",
        data={"username": "loginuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client):
    client.post(
        "/signup",
        json={"username": "wrongpass", "email": "wrongpass@example.com", "password": "password123"},
    )
    response = client.post(
        "/token",
        data={"username": "wrongpass", "password": "incorrect"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_get_current_user(client):
    client.post(
        "/signup",
        json={"username": "currentuser", "email": "current@example.com", "password": "password123"},
    )
    login_res = client.post("/token", data={"username": "currentuser", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "currentuser"
    assert data["email"] == "current@example.com"
