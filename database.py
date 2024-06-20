from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decouple import config

SQLALCHEMY_DATABASE_URL = config("POSTGRESQL_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False,
    pool_recycle=3600,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
