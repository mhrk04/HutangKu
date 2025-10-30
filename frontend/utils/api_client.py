"""
API Client - Helper functions to make HTTP calls to FastAPI backend
"""
import requests
from typing import List, Dict, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from core.config import settings

class APIClient:
    """Client for interacting with the Debt Management API"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or settings.API_BASE_URL
        self.debts_endpoint = f"{self.base_url}/debts"
        self.companies_endpoint = f"{self.base_url}/companies"
    
    def get_all_debts(self, status: Optional[str] = None) -> List[Dict]:
        """Retrieve all debts, optionally filtered by status"""
        try:
            params = {"status": status} if status else {}
            response = requests.get(self.debts_endpoint, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching debts: {e}")
            return []
    
    def get_debt(self, debt_id: str) -> Optional[Dict]:
        """Retrieve a single debt by ID"""
        try:
            response = requests.get(f"{self.debts_endpoint}/{debt_id}", timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching debt {debt_id}: {e}")
            return None
    
    def create_debt(self, debt_data: Dict) -> Optional[Dict]:
        """Create a new debt record"""
        try:
            response = requests.post(self.debts_endpoint, json=debt_data, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating debt: {e}")
            return None
    
    def update_debt(self, debt_id: str, debt_data: Dict) -> Optional[Dict]:
        """Update an existing debt record"""
        try:
            response = requests.put(
                f"{self.debts_endpoint}/{debt_id}",
                json=debt_data,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error updating debt {debt_id}: {e}")
            return None
    
    def delete_debt(self, debt_id: str) -> bool:
        """Delete a debt record"""
        try:
            response = requests.delete(f"{self.debts_endpoint}/{debt_id}", timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting debt {debt_id}: {e}")
            return False
    
    def mark_debt_paid(self, debt_id: str) -> Optional[Dict]:
        """Quick action to mark a debt as paid off"""
        return self.update_debt(debt_id, {"status": "Paid Off"})
    
    # ============ COMPANY OPERATIONS ============
    
    def get_all_companies(self) -> List[str]:
        """Retrieve all custom company names"""
        try:
            response = requests.get(self.companies_endpoint, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching companies: {e}")
            return []
    
    def create_company(self, company_name: str) -> Optional[Dict]:
        """Add a new custom company"""
        try:
            response = requests.post(
                self.companies_endpoint,
                json={"name": company_name},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating company: {e}")
            return None
    
    def delete_company(self, company_id: str) -> bool:
        """Delete a custom company"""
        try:
            response = requests.delete(
                f"{self.companies_endpoint}/{company_id}",
                timeout=5
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error deleting company {company_id}: {e}")
            return False
    
    def get_company_by_name(self, company_name: str) -> Optional[Dict]:
        """Get company details by name"""
        try:
            response = requests.get(
                f"{self.companies_endpoint}/by-name/{company_name}",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching company {company_name}: {e}")
            return None