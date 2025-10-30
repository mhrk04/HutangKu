"""
CRUD operations for debt records in MongoDB
"""
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo import ReturnDocument
from .connection import get_collection

def debt_helper(debt) -> dict:
    """Convert MongoDB document to dictionary"""
    return {
        "id": str(debt["_id"]),
        "company_name": debt["company_name"],
        "amount_owed": debt["amount_owed"],
        "minimum_payment": debt["minimum_payment"],
        "due_date": debt["due_date"],
        "status": debt["status"],
        "notes": debt.get("notes", "")
    }

async def create_debt(debt_data: dict) -> dict:
    """Create a new debt record"""
    collection = get_collection()
    result = await collection.insert_one(debt_data)
    new_debt = await collection.find_one({"_id": result.inserted_id})
    return debt_helper(new_debt)

async def get_debt(debt_id: str) -> Optional[dict]:
    """Retrieve a single debt record by ID"""
    collection = get_collection()
    debt = await collection.find_one({"_id": ObjectId(debt_id)})
    if debt:
        return debt_helper(debt)
    return None

async def get_all_debts(status: Optional[str] = None) -> List[dict]:
    """Retrieve all debt records, optionally filtered by status"""
    collection = get_collection()
    query = {}
    if status:
        query["status"] = status
    
    debts = []
    async for debt in collection.find(query):
        debts.append(debt_helper(debt))
    return debts

async def update_debt(debt_id: str, debt_data: dict) -> Optional[dict]:
    """Update an existing debt record"""
    collection = get_collection()
    
    # Remove None values from update data
    update_data = {k: v for k, v in debt_data.items() if v is not None}
    
    if not update_data:
        return None
    
    updated_debt = await collection.find_one_and_update(
        {"_id": ObjectId(debt_id)},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER
    )
    
    if updated_debt:
        return debt_helper(updated_debt)
    return None

async def delete_debt(debt_id: str) -> bool:
    """Delete a debt record"""
    collection = get_collection()
    result = await collection.delete_one({"_id": ObjectId(debt_id)})
    return result.deleted_count > 0

# ============ COMPANY OPERATIONS ============

def company_helper(company) -> dict:
    """Convert MongoDB company document to dictionary"""
    return {
        "id": str(company["_id"]),
        "name": company["name"]
    }

async def get_companies_collection():
    """Get the companies collection"""
    from .connection import get_database
    db = get_database()
    return db["companies"]

async def get_all_companies() -> List[str]:
    """Retrieve all company names"""
    collection = await get_companies_collection()
    companies = []
    async for company in collection.find().sort("name", 1):
        companies.append(company["name"])
    return companies

async def add_company(company_name: str) -> dict:
    """Add a new company name"""
    collection = await get_companies_collection()
    
    # Check if company already exists
    existing = await collection.find_one({"name": company_name})
    if existing:
        return company_helper(existing)
    
    # Insert new company
    result = await collection.insert_one({"name": company_name})
    new_company = await collection.find_one({"_id": result.inserted_id})
    return company_helper(new_company)

async def delete_company(company_id: str) -> bool:
    """Delete a company"""
    collection = await get_companies_collection()
    result = await collection.delete_one({"_id": ObjectId(company_id)})
    return result.deleted_count > 0

async def get_company_by_name(company_name: str) -> Optional[dict]:
    """Get company by name"""
    collection = await get_companies_collection()
    company = await collection.find_one({"name": company_name})
    if company:
        return company_helper(company)
    return None