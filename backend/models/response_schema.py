"""
Standard API response schemas
"""
from pydantic import BaseModel
from typing import Optional, Any

class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    status_code: int = 400

class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str
    data: Optional[Any] = None

class DeleteResponse(BaseModel):
    """Response for delete operations"""
    message: str
    deleted_id: str