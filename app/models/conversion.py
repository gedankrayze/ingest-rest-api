from pydantic import BaseModel
from typing import Optional, Dict, Any

class ConversionResponse(BaseModel):
    filename: str
    original_format: str
    markdown_content: str
    metadata: Optional[Dict[str, Any]] = None
    conversion_time: float

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None