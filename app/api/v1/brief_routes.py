from fastapi import APIRouter, HTTPException, Query, Depends
from app.models.brief import BriefRequest, BriefResponse, PaginatedBriefs
from app.services.scheduler import run_scheduled_brief
from app.services.brief_generator import fetch_brief_from_openai
from app.security.dependencies import verify_scheduler_api_key
from app.db.crud import get_recent_briefs, insert_brief
from datetime import datetime
import logging

router = APIRouter(prefix="/api/v1/briefs", tags=["Briefs"])

@router.post("/", response_model=BriefResponse, summary="Generate a new brief", description="Creates a new AI-generated brief based on the given topics and tone.")
def generate_brief(request: BriefRequest):
    prompt = f"Write a daily brief on: {request.topics}, in a {request.tone} tone."

    # Let fetch_brief_from_openai handle exceptions internally
    content = fetch_brief_from_openai(prompt)

    created_at = datetime.utcnow().isoformat()
    try:
        brief_id = insert_brief(request.topics, request.tone, content, created_at)
    except Exception as e:
        logging.error(f"Database insert failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to save brief to database.")
    
    return BriefResponse(id=brief_id, content=content, created_at=created_at)


@router.get("/", response_model=PaginatedBriefs, summary="Get briefs", description="Returns a paginated list of recent briefs.")
def get_briefs(
    limit: int = Query(10, ge=1, le=50, description="Number of briefs to return (max 50)"), 
    offset: int = Query(0, ge=0, description="Number of briefs to skip (for pagination)")
):
    logging.info(f"Querying briefs with limit={limit}, offset={offset}")
    return get_recent_briefs(limit=limit, offset=offset)


@router.post("/run-schedule", summary="Run scheduled brief generation", description="Triggers the scheduled generation of a brief with default content (requires API key).")
def run_scheduled_brief_route():
    # Any exceptions here will be caught globally or handled in brief_generator
    brief_id = run_scheduled_brief(topics="daily news", tone="neutral")
    return {"message": f"Scheduled brief created with ID {brief_id}"}
