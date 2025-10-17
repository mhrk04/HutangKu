"""
API Router for debt management endpoints
Implements POST, GET, PUT, DELETE operations for /debts
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.models.debt_schema import DebtCreate, DebtUpdate, DebtResponse
from backend.models.response_schema import SuccessResponse, DeleteResponse
from backend.database import crud_db

router = APIRouter()

@router.post("", response_model=DebtResponse, status_code=201)
async def create_debt(debt: DebtCreate):
    """Create a new debt record"""
    try:
        debt_dict = debt.model_dump()
        # Convert date to string for MongoDB storage
        debt_dict["due_date"] = debt_dict["due_date"].isoformat()
        debt_dict["status"] = debt_dict["status"].value  # Convert enum to string
        
        new_debt = await crud_db.create_debt(debt_dict)
        return new_debt
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating debt: {str(e)}")

@router.get("", response_model=List[DebtResponse])
async def get_all_debts(status: Optional[str] = Query(None, description="Filter by status")):
    """Retrieve all debt records, optionally filtered by status"""
    try:
        debts = await crud_db.get_all_debts(status=status)
        return debts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving debts: {str(e)}")

@router.get("/{debt_id}", response_model=DebtResponse)
async def get_debt(debt_id: str):
    """Retrieve a single debt record by ID"""
    try:
        debt = await crud_db.get_debt(debt_id)
        if not debt:
            raise HTTPException(status_code=404, detail=f"Debt with id {debt_id} not found")
        return debt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving debt: {str(e)}")

@router.put("/{debt_id}", response_model=DebtResponse)
async def update_debt(debt_id: str, debt: DebtUpdate):
    """Update an existing debt record"""
    try:
        debt_dict = debt.model_dump(exclude_none=True)
        
        # Convert date to string if present
        if "due_date" in debt_dict and debt_dict["due_date"]:
            debt_dict["due_date"] = debt_dict["due_date"].isoformat()
        
        # Convert enum to string if present
        if "status" in debt_dict and debt_dict["status"]:
            debt_dict["status"] = debt_dict["status"].value
        
        updated_debt = await crud_db.update_debt(debt_id, debt_dict)
        if not updated_debt:
            raise HTTPException(status_code=404, detail=f"Debt with id {debt_id} not found")
        return updated_debt
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating debt: {str(e)}")

@router.delete("/{debt_id}", response_model=DeleteResponse)
async def delete_debt(debt_id: str):
    """Delete a debt record"""
    try:
        success = await crud_db.delete_debt(debt_id)
        if not success:
            raise HTTPException(status_code=404, detail=f"Debt with id {debt_id} not found")
        return DeleteResponse(message="Debt deleted successfully", deleted_id=debt_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting debt: {str(e)}")