from openai import OpenAI
from fastapi import HTTPException
import os
import logging

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_brief_from_openai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except HTTPException as he:
        raise he  #let FastAPI handle it natively
    except Exception as e:
        logging.error(f"OpenAI call failed: {e}")
        raise RuntimeError(status_code=500,detail="AI generation failed.")
