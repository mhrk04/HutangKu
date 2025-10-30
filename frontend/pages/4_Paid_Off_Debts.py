"""
Paid Off Debts Page - View and manage paid off debts
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from frontend.utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="Paid Off Debts - HutangKu",
    page_icon="✅",
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
    st.title("✅ Paid Off Debts")
    st.markdown("View all your successfully paid off debts")
    st.markdown("---")
    
    # Show success message if any
    if st.session_state.show_success:
        st.success(st.session_state.success_message)
        st.session_state.show_success = False
    
    # Fetch paid off debts
    paid_debts = api_client.get_all_debts(status="Paid Off")
    
    if not paid_debts:
        st.info("🎉 No paid off debts yet. Once you mark debts as paid, they will appear here.")
    else:
        st.success(f"**Total Paid Off Debts:** {len(paid_debts)}")
        
        # Calculate total paid amount
        total_paid = sum(debt['amount_owed'] for debt in paid_debts)
        st.metric("Total Amount Paid Off", f"RM {total_paid:,.2f}")
        
        st.markdown("---")
        
        # Display each paid off debt
        for debt in paid_debts:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.write(f"**{debt['company_name']}**")
                    if debt.get('notes'):
                        st.caption(f"📝 {debt['notes']}")
                
                with col2:
                    st.write(f"**Amount:** RM {debt['amount_owed']:,.2f}")
                    st.caption(f"Min Payment: RM {debt['minimum_payment']:,.2f}")
                
                with col3:
                    due_date_obj = datetime.fromisoformat(debt['due_date']).date()
                    st.write(f"**Due Date:** {due_date_obj.strftime('%d %b %Y')}")
                    st.caption(f"✅ Status: {debt['status']}")
                
                with col4:
                    if st.button("🗑️ Delete", key=f"delete_paid_{debt['id']}", help="Permanently delete this record", use_container_width=True):
                        if api_client.delete_debt(debt['id']):
                            st.session_state.success_message = f"🗑️ Debt record '{debt['company_name']}' deleted!"
                            st.session_state.show_success = True
                            st.rerun()
                
                st.divider()
    
    # Refresh button in sidebar
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

if __name__ == "__main__":
    main()
