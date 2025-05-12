from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# Pydantic input/output models for validation and API I/O
class ToneEnum(str, Enum):
    neutral = "neutral"
    casual = "casual"
    professional = "professional"

class BriefRequest(BaseModel):
    topics: str = Field(..., min_length=1, max_length=1000)
    tone: ToneEnum = ToneEnum.neutral

class BriefResponse(BaseModel):
    id: int
    content: str
    created_at: str

class PaginatedBriefs(BaseModel):
    total: int
    limit: int
    offset: int
    has_more: bool
    briefs: List[BriefResponse]
