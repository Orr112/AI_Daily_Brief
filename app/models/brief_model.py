from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Brief(Base):
    __tablename__ = "briefs"

    id = Column(Integer, primary_key=True, index=True)
    topics = Column(String(255), nullable=False)
    tone = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(String, nullable=False)
