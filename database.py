from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decouple import config

SQLALCHEMY_DATABASE_URL = config("POSTGRESQL_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    pool_size=20,
    max_overflow=0
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
