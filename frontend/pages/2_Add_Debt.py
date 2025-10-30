"""
Add Debt Page - Simple debt entry with company dropdown
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

# Predefined list of common BNPL and financial companies in Malaysia
COMMON_COMPANIES = [
    "Atome",
    "Grab PayLater",
    "Shopee PayLater",
    "Lazada PayLater",
    "Pace",
    "Rely",
    "Hoolah",
    "Maybank",
    "CIMB",
    "Public Bank",
    "RHB Bank",
    "Hong Leong Bank",
    "AmBank",
    "OCBC",
    "UOB",
    "Standard Chartered",
    "HSBC",
    "Citibank",
    "Others (Type manually)"
]

# Initialize session state
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_message' not in st.session_state:
    st.session_state.success_message = ""


def get_company_list():
    """Get the combined list of predefined and custom companies from database"""
    # Get custom companies from database
    custom_companies = api_client.get_all_companies()
    
    # Combine predefined companies with custom ones (excluding "Others")
    base_companies = [c for c in COMMON_COMPANIES if c != "Others (Type manually)"]
    all_companies = base_companies + custom_companies
    
    # Remove duplicates while preserving order
    seen = set()
    unique_companies = []
    for company in all_companies:
        if company not in seen:
            seen.add(company)
            unique_companies.append(company)
    
    # Sort the list alphabetically
    unique_companies.sort()
    
    # Add "Others" at the end
    unique_companies.append("Others (Type manually)")
    return unique_companies


def main():
    st.title("➕ Add New Debt")
    st.markdown("Create a new debt entry")
    st.markdown("---")
    
    # Show success message if any
    if st.session_state.show_success:
        st.success(st.session_state.success_message)
        st.session_state.show_success = False
    
    # Company selection outside form to allow dynamic input
    selected_company = st.selectbox(
        "Company *", 
        options=get_company_list(),
        help="Select a company or choose 'Others' to type manually",
        key="company_select"
    )
    
    # Show text input if "Others" selected
    if selected_company == "Others (Type manually)":
        company_name_input = st.text_input("Company Name *", placeholder="e.g., Boost, TNG eWallet", key="custom_company")
    else:
        company_name_input = selected_company
        st.info(f"Selected: **{selected_company}**")
    
    # Main form
    with st.form(key="add_debt_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Use the company name from above
            company_name = company_name_input
            
            amount_owed = st.number_input("Amount Owed (RM) *", min_value=0.01, step=0.01, format="%.2f")
            minimum_payment = st.number_input("Minimum Payment (RM) *", min_value=0.01, step=0.01, format="%.2f")
        
        with col2:
            due_date = st.date_input("Due Date *", min_value=date.today())
            status = st.selectbox("Status *", ["Active Debt", "Paid Off"], index=0)
            notes = st.text_area("Notes (Optional)", placeholder="Account number, installment plan, etc.")
        
        submit_button = st.form_submit_button("➕ Add Debt", use_container_width=True)
        
        if submit_button:
            if not company_name:
                st.error("Company name required!")
            elif amount_owed <= 0:
                st.error("Amount owed must be greater than 0!")
            elif minimum_payment <= 0:
                st.error("Minimum payment must be greater than 0!")
            else:
                # If it's a custom company, add it to the database
                if selected_company == "Others (Type manually)" and company_name:
                    # Check if not in predefined list
                    if company_name not in COMMON_COMPANIES:
                        result = api_client.create_company(company_name)
                        if result:
                            st.session_state.success_message = f"✅ Company '{company_name}' added to your company list!"
                
                # Resolve potential tuple from st.date_input to satisfy linter
                final_due_date = due_date[0] if isinstance(due_date, tuple) else due_date

                result = api_client.create_debt({
                    "company_name": company_name,
                    "amount_owed": amount_owed,
                    "minimum_payment": minimum_payment,
                    "due_date": final_due_date.isoformat() if final_due_date else None,
                    "status": status,
                    "notes": notes
                })
                if result:
                    st.session_state.success_message = f"✅ Debt '{company_name}' added successfully!"
                    st.session_state.show_success = True
                    st.rerun()
                else:
                    st.error("Failed to create debt. Please check the backend is running.")
    
    st.markdown("---")
    st.info("💡 After adding a debt, go to 'Active Debts' page to view and manage it.")
    
    # Show custom companies management
    st.markdown("---")
    st.subheader("📝 Manage Custom Companies")
    
    custom_companies = api_client.get_all_companies()
    
    if custom_companies:
        st.write("**Your Custom Companies:**")
        st.caption("These are companies you've added that aren't in the default list.")
        
        for company in custom_companies:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {company}")
            with col2:
                # Get company details to get its ID
                company_details = api_client.get_company_by_name(company)
                if company_details and st.button("🗑️", key=f"delete_company_{company}", help=f"Delete {company}"):
                    if api_client.delete_company(company_details['id']):
                        st.success(f"Deleted '{company}' from your company list!")
                        st.rerun()
                    else:
                        st.error(f"Failed to delete '{company}'")
    else:
        st.info("No custom companies yet. Add one by selecting 'Others (Type manually)' when creating a debt.")
    
    # Refresh button in sidebar
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()


if __name__ == "__main__":
    main()
