import logging
from typing import List, Dict
from app.db.database import SessionLocal
from app.models.brief_model import Brief

def get_recent_briefs(limit: int = 10, offset: int = 0) -> dict:
    db = SessionLocal()
    try:
        total = db.query(Brief).count()
        rows = db.query(Brief).order_by(Brief.created_at.desc()).offset(offset).limit(limit).all()

        data = [
            {"id": brief.id, "content": brief.content, "created_at": brief.created_at}
            for brief in rows
        ]

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total,
            "briefs": data
        }
    finally:
        db.close()

def insert_brief(topics, tone, content, created_at):
    db = SessionLocal()
    try:
        brief = Brief(topics=topics, tone=tone, content=content, created_at=created_at)
        db.add(brief)
        db.commit()
        db.refresh(brief)
        return brief.id
    finally:
        db.close()
