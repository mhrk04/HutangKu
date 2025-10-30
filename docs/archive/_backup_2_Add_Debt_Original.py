"""
Manage Debts Page - Add new debts
"""
import streamlit as st
import sys
import os
from datetime import date

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from frontend.utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="Add Debt - HutangKu",
    page_icon="➕",
    layout="wide"
)

# Initialize API client
api_client = APIClient()

# Initialize session state for messages
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_message' not in st.session_state:
    st.session_state.success_message = ""

def main():
    st.title("➕ Add New Debt")
    st.markdown("Create a new debt entry")
    st.markdown("---")
    
    # Show success message if any
    if st.session_state.show_success:
        st.success(st.session_state.success_message)
        st.session_state.show_success = False
    
    # === CREATION FORM ===
    with st.form(key="creation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name *", placeholder="e.g., Atome, Shopee")
            amount_owed = st.number_input("Amount Owed (RM) *", min_value=0.01, step=0.01, format="%.2f")
            minimum_payment = st.number_input("Minimum Payment (RM) *", min_value=0.01, step=0.01, format="%.2f")
        
        with col2:
            due_date = st.date_input("Due Date *", min_value=date.today())
            status = st.selectbox("Status *", ["Active Debt", "Paid Off"], index=0)
            notes = st.text_area("Notes (Optional)", placeholder="Account number, installment plan, etc.")
        
        submit_button = st.form_submit_button("➕ Add Debt", use_container_width=True)
        
        if submit_button:
            if not company_name:
                st.error("Please enter a company name!")
            elif amount_owed <= 0:
                st.error("Amount owed must be greater than 0!")
            elif minimum_payment <= 0:
                st.error("Minimum payment must be greater than 0!")
            else:
                debt_data = {
                    "company_name": company_name,
                    "amount_owed": amount_owed,
                    "minimum_payment": minimum_payment,
                    "due_date": due_date.isoformat() if due_date else None,
                    "status": status,
                    "notes": notes
                }
                
                result = api_client.create_debt(debt_data)
                if result:
                    st.session_state.success_message = f"✅ Debt '{company_name}' added successfully!"
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("Failed to create debt. Please check the backend is running.")
    
    st.markdown("---")
    st.info("💡 After adding a debt, go to 'Active Debts' page to view and manage it.")
    
    # Refresh button in sidebar
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

if __name__ == "__main__":
    main()