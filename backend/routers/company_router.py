"""
Company Router - API endpoints for managing custom companies
"""
from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from backend.database.crud_db import (
    get_all_companies,
    add_company,
    delete_company,
    get_company_by_name
)

router = APIRouter(prefix="/companies", tags=["companies"])

class CompanyCreate(BaseModel):
    name: str

class CompanyResponse(BaseModel):
    id: str
    name: str

@router.get("/", response_model=List[str])
async def list_companies():
    """Get all custom company names"""
    try:
        companies = await get_all_companies()
        return companies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=CompanyResponse)
async def create_company(company: CompanyCreate):
    """Add a new custom company"""
    try:
        result = await add_company(company.name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{company_id}")
async def remove_company(company_id: str):
    """Delete a custom company"""
    try:
        success = await delete_company(company_id)
        if not success:
            raise HTTPException(status_code=404, detail="Company not found")
        return {"message": "Company deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-name/{company_name}", response_model=CompanyResponse)
async def get_company(company_name: str):
    """Get company details by name"""
    try:
        company = await get_company_by_name(company_name)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
