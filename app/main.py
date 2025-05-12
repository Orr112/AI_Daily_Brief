from fastapi import FastAPI
from app.api.v1.routes import router
from app.db.database import init_db
from dotenv import load_dotenv
from fastapi.responses import  JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import HTTPException
import logging



load_dotenv()
logging.basicConfig(level=logging.INFO)
logging.info("FastAPI app starting...")

app = FastAPI(title="Daily Brief API",
    description="An API for generating and retrieving AI-powered daily briefs.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Briefs", "description": "Generate and retrieve AI-generated briefs"},
        {"name": "Scheduler", "description": "Trigger brief creation via scheduler"},
        {"name": "Health", "description": "Health and uptime checks"}
    ]
)

init_db()

app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"[UNCAUGHT ERROR] {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred.  Please try again later."}
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )