"""
Pydantic schemas for Debt records - defines structure and validation
"""
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional
from enum import Enum

class DebtStatus(str, Enum):
    """Allowed debt status values"""
    ACTIVE = "Active Debt"
    PAID_OFF = "Paid Off"

class DebtBase(BaseModel):
    """Base debt schema with common fields"""
    company_name: str = Field(..., min_length=1, description="Name of the creditor/company")
    amount_owed: float = Field(..., gt=0, description="Current outstanding balance")
    minimum_payment: float = Field(..., gt=0, description="Minimum payment required")
    due_date: date = Field(..., description="Payment due date")
    status: DebtStatus = Field(default=DebtStatus.ACTIVE, description="Debt status")
    notes: Optional[str] = Field(default="", description="Optional notes or account numbers")

class DebtCreate(DebtBase):
    """Schema for creating a new debt record"""
    pass

class DebtUpdate(BaseModel):
    """Schema for updating an existing debt record - all fields optional"""
    company_name: Optional[str] = Field(None, min_length=1)
    amount_owed: Optional[float] = Field(None, gt=0)
    minimum_payment: Optional[float] = Field(None, gt=0)
    due_date: Optional[date] = None
    status: Optional[DebtStatus] = None
    notes: Optional[str] = None

class DebtResponse(DebtBase):
    """Schema for debt record responses"""
    id: str = Field(..., description="MongoDB document ID as string")
    
    class Config:
        from_attributes = True