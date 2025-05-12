from fastapi import Header, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()
EXPECTED_KEY = os.getenv("SCHEDULER_API_KEY")

def verify_scheduler_api_key(x_api_key: str = Header(...)):
    if x_api_key != EXPECTED_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key"
        )
