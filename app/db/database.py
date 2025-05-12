from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.brief_model import Base
import os

DB_URL = os.getenv("DB_URL", "sqlite:///./briefs.db")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
