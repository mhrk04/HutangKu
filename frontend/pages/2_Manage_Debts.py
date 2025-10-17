"""
Manage Debts Page - CRUD operations
Create, Update, Delete debt records
"""
import streamlit as st
import sys
import os
from datetime import datetime, date

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from frontend.utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="Manage Debts - HutangKu - Debt Management",
    page_icon="✏️",
    layout="wide"
)

# Initialize API client
api_client = APIClient()

# Initialize session state for edit mode
if 'edit_debt_id' not in st.session_state:
    st.session_state.edit_debt_id = None
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_message' not in st.session_state:
    st.session_state.success_message = ""

def main():
    st.title("✏️ Manage Debts")
    st.markdown("---")
    
    # Show success message if any
    if st.session_state.show_success:
        st.success(st.session_state.success_message)
        st.session_state.show_success = False
    
    # === CREATION FORM ===
    st.header("➕ Add New Debt")
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
                    "due_date": due_date.isoformat(),
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
    
    # === EDIT/DELETE SECTION ===
    st.header("📋 Active Debts")
    
    # Fetch active debts
    debts = api_client.get_all_debts(status="Active Debt")
    
    if not debts:
        st.info("No active debts found. Add your first debt using the form above.")
    else:
        # Display each debt with actions
        for debt in debts:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1.5, 1.5, 1, 1])
                
                with col1:
                    st.write(f"**{debt['company_name']}**")
                    if debt.get('notes'):
                        st.caption(f"📝 {debt['notes']}")
                
                with col2:
                    st.write(f"**Owed:** RM {debt['amount_owed']:.2f}")
                    st.caption(f"Min: RM {debt['minimum_payment']:.2f}")
                
                with col3:
                    due_date_obj = datetime.fromisoformat(debt['due_date']).date()
                    st.write(f"**Due:** {due_date_obj.strftime('%d %b %Y')}")
                    days_until = (due_date_obj - date.today()).days
                    if days_until < 0:
                        st.caption(f"⚠️ Overdue by {abs(days_until)} days")
                    elif days_until <= 7:
                        st.caption(f"⚠️ Due in {days_until} days")
                
                with col4:
                    if st.button("✏️ Edit", key=f"edit_{debt['id']}", use_container_width=True):
                        st.session_state.edit_debt_id = debt['id']
                        st.rerun()
                    
                    if st.button("✅ Paid", key=f"paid_{debt['id']}", use_container_width=True):
                        result = api_client.mark_debt_paid(debt['id'])
                        if result:
                            st.session_state.success_message = f"✅ Debt '{debt['company_name']}' marked as paid!"
                            st.session_state.show_success = True
                            st.rerun()
                
                with col5:
                    if st.button("🗑️ Delete", key=f"delete_{debt['id']}", use_container_width=True):
                        if api_client.delete_debt(debt['id']):
                            st.session_state.success_message = f"🗑️ Debt '{debt['company_name']}' deleted!"
                            st.session_state.show_success = True
                            st.rerun()
                
                st.divider()
    
    # === EDIT FORM (appears when edit button is clicked) ===
    if st.session_state.edit_debt_id:
        st.markdown("---")
        st.header("✏️ Edit Debt")
        
        # Fetch the debt to edit
        debt_to_edit = api_client.get_debt(st.session_state.edit_debt_id)
        
        if debt_to_edit:
            with st.form(key="edit_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    edit_company = st.text_input("Company Name", value=debt_to_edit['company_name'])
                    edit_amount = st.number_input("Amount Owed (RM)", value=debt_to_edit['amount_owed'], min_value=0.01, step=0.01, format="%.2f")
                    edit_min_payment = st.number_input("Minimum Payment (RM)", value=debt_to_edit['minimum_payment'], min_value=0.01, step=0.01, format="%.2f")
                
                with col2:
                    edit_due_date = st.date_input("Due Date", value=datetime.fromisoformat(debt_to_edit['due_date']).date())
                    edit_status = st.selectbox("Status", ["Active Debt", "Paid Off"], index=0 if debt_to_edit['status'] == "Active Debt" else 1)
                    edit_notes = st.text_area("Notes", value=debt_to_edit.get('notes', ''))
                
                col_update, col_cancel = st.columns([1, 1])
                
                with col_update:
                    update_button = st.form_submit_button("💾 Update Debt", use_container_width=True)
                
                with col_cancel:
                    cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)
                
                if update_button:
                    update_data = {
                        "company_name": edit_company,
                        "amount_owed": edit_amount,
                        "minimum_payment": edit_min_payment,
                        "due_date": edit_due_date.isoformat(),
                        "status": edit_status,
                        "notes": edit_notes
                    }
                    
                    result = api_client.update_debt(st.session_state.edit_debt_id, update_data)
                    if result:
                        st.session_state.success_message = f"✅ Debt '{edit_company}' updated successfully!"
                        st.session_state.show_success = True
                        st.session_state.edit_debt_id = None
                        st.rerun()
                    else:
                        st.error("Failed to update debt.")
                
                if cancel_button:
                    st.session_state.edit_debt_id = None
                    st.rerun()
        else:
            st.error("Debt not found.")
            st.session_state.edit_debt_id = None
    
    # === PAID OFF DEBTS SECTION ===
    st.markdown("---")
    with st.expander("📦 View Paid Off Debts"):
        paid_debts = api_client.get_all_debts(status="Paid Off")
        
        if not paid_debts:
            st.info("No paid off debts.")
        else:
            for debt in paid_debts:
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.write(f"**{debt['company_name']}**")
                    if debt.get('notes'):
                        st.caption(f"📝 {debt['notes']}")
                
                with col2:
                    st.write(f"Amount: RM {debt['amount_owed']:.2f}")
                    st.caption(f"Status: {debt['status']}")
                
                with col3:
                    if st.button("🗑️", key=f"delete_paid_{debt['id']}", help="Delete this record"):
                        if api_client.delete_debt(debt['id']):
                            st.rerun()
                
                st.divider()
    
    # Refresh button
    # st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

if __name__ == "__main__":
    main()