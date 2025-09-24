import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from vault_client import VaultClient

vault = VaultClient()
creds = vault.get_creds("db_creds")

if os.getenv("DOCKER_ENV"):
    DATABASE_URL = f"postgresql://{creds['username']}:{creds['password']}@{os.environ['SERVER_DB_URL']}/movie_booking"
else:
    DATABASE_URL = f"postgresql://{creds['username']}:{creds['password']}@{os.environ['DB_URL']}/movie_booking"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
