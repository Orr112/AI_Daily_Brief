from fastapi import APIRouter
from app.db.database import engine
from sqlalchemy import text

router = APIRouter(prefix="/api/v1", tags=["Health"])

@router.get("/health", tags=["Health"])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        return {"status": "ok", "database": "unreachable"}