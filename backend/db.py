from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# ======================
# SQLALCHEMY ENGINE
# ======================
engine = create_engine(
    DATABASE_URL,
    echo=False,        # True karoge to SQL logs dikhenge
    pool_pre_ping=True
)

# ======================
# SESSION
# ======================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ======================
# BASE CLASS FOR MODELS
# ======================
Base = declarative_base()

# ======================
# DB DEPENDENCY (FastAPI)
# ======================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
