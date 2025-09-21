import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def client():
    """
    Start a temporary PostgreSQL container and provide a TestClient
    with an isolated database for all tests.
    """
    with PostgresContainer("postgres:15-alpine") as postgres:
        # Create SQLAlchemy engine
        engine = create_engine(postgres.get_connection_url())
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

        # Create tables via SQLAlchemy (no SQL file mount needed)
        Base.metadata.create_all(bind=engine)

        # Override FastAPI dependency
        def override_get_db():
            db = TestingSessionLocal()
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        # Provide FastAPI TestClient
        yield TestClient(app)

        # Drop tables after tests
        Base.metadata.drop_all(bind=engine)