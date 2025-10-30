"""
Active Debts Page - View, edit, delete, and mark debts as paid
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
    page_title="Active Debts - HutangKu",
    page_icon="📋",
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
if 'show_edit_dialog' not in st.session_state:
    st.session_state.show_edit_dialog = False


@st.dialog("✏️ Edit Debt", width="large")
def edit_debt_dialog(debt_to_edit):
    """Edit debt form in a popup dialog"""
    with st.form(key="edit_form"):
        col1, col2 = st.columns(2)

        with col1:
            edit_company = st.text_input("Company Name", value=debt_to_edit['company_name'])
            edit_amount = st.number_input(
                "Amount Owed (RM)",
                value=debt_to_edit['amount_owed'],
                min_value=0.01,
                step=0.01,
                format="%.2f"
            )
            edit_min_payment = st.number_input(
                "Minimum Payment (RM)",
                value=debt_to_edit['minimum_payment'],
                min_value=0.01,
                step=0.01,
                format="%.2f"
            )

        with col2:
            edit_due_date = st.date_input(
                "Due Date",
                value=datetime.fromisoformat(debt_to_edit['due_date']).date()
            )
            edit_status = st.selectbox(
                "Status",
                ["Active Debt", "Paid Off"],
                index=0 if debt_to_edit['status'] == "Active Debt" else 1
            )
            edit_notes = st.text_area("Notes", value=debt_to_edit.get('notes', ''))

        col_update, col_cancel = st.columns([1, 1])

        with col_update:
            update_button = st.form_submit_button("💾 Update Debt", use_container_width=True)

        with col_cancel:
            cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)

        if update_button:
            # Resolve potential tuple from st.date_input to satisfy linter
            final_due_date = edit_due_date if isinstance(edit_due_date, date) else edit_due_date

            update_data = {
                "company_name": edit_company,
                "amount_owed": edit_amount,
                "minimum_payment": edit_min_payment,
                "due_date": final_due_date.isoformat() if final_due_date else None,
                "status": edit_status,
                "notes": edit_notes
            }

            result = api_client.update_debt(st.session_state.edit_debt_id, update_data)
            if result:
                st.session_state.success_message = f"✅ Debt '{edit_company}' updated successfully!"
                st.session_state.show_success = True
                st.session_state.edit_debt_id = None
                st.session_state.show_edit_dialog = False
                st.rerun()
            else:
                st.error("Failed to update debt.")

        if cancel_button:
            st.session_state.edit_debt_id = None
            st.session_state.show_edit_dialog = False
            st.rerun()


def main():
    st.title("📋 Active Debts")
    st.markdown("View and manage your active debts")
    st.markdown("---")

    # Show success message if any
    if st.session_state.show_success:
        st.success(st.session_state.success_message)
        st.session_state.show_success = False

    # Fetch active debts
    debts = api_client.get_all_debts(status="Active Debt")

    if not debts:
        st.info("No active debts found. Add your first debt from the Manage Debts page.")
    else:
        # Show summary metrics
        total_owed = sum(debt['amount_owed'] for debt in debts)
        total_min_payment = sum(debt['minimum_payment'] for debt in debts)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Active Debts", len(debts))
        with col2:
            st.metric("Total Amount Owed", f"RM {total_owed:,.2f}")
        with col3:
            st.metric("Total Min Payment", f"RM {total_min_payment:,.2f}")

        st.markdown("---")

        # Display debts sorted by due date
        st.subheader("📅 Debts Sorted by Due Date")
        
        # Sort all debts by due date (nearest first)
        sorted_debts = sorted(debts, key=lambda d: datetime.fromisoformat(d['due_date']))
        
        # Display each debt
        for debt in sorted_debts:
            due_date_obj = datetime.fromisoformat(debt['due_date']).date()
            due_date_display = due_date_obj.strftime("%d %b %Y")
            days_until_due = (due_date_obj - date.today()).days
            
            # Color code based on urgency
            if days_until_due >= 0 and days_until_due <= 7:
                if days_until_due == 0:
                    st.markdown(f"🔴 **URGENT** - Payment DUE TODAY!")
                elif days_until_due == 1:
                    st.markdown(f"🔴 **URGENT** - Payment due TOMORROW!")
                else:
                    st.markdown(f"🔴 **URGENT** - Due in {days_until_due} days")
            elif days_until_due < 0:
                st.markdown(f"🔴 **OVERDUE by {abs(days_until_due)} days!**")
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1.5])
            
            with col1:
                st.write(f"**🏢 {debt['company_name']}**")
                if debt.get('notes'):
                    st.caption(f"📝 {debt['notes']}")
            
            with col2:
                st.write("**Amount Owed:**")
                st.write(f"RM {debt['amount_owed']:,.2f}")
                st.caption(f"Min: RM {debt['minimum_payment']:,.2f}")
            
            with col3:
                st.write("**Due Date:**")
                st.write(due_date_display)
            
            with col4:
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                
                with btn_col1:
                    if st.button("✏️", key=f"edit_{debt['id']}", help="Edit"):
                        st.session_state.edit_debt_id = debt['id']
                        st.session_state.show_edit_dialog = True
                        st.rerun()
                
                with btn_col2:
                    if st.button("✅", key=f"paid_{debt['id']}", help="Mark Paid"):
                        result = api_client.mark_debt_paid(debt['id'])
                        if result:
                            st.session_state.success_message = f"✅ Debt '{debt['company_name']}' marked as paid!"
                            st.session_state.show_success = True
                            st.rerun()
                
                with btn_col3:
                    if st.button("🗑️", key=f"delete_{debt['id']}", help="Delete"):
                        if api_client.delete_debt(debt['id']):
                            st.session_state.success_message = f"🗑️ Debt '{debt['company_name']}' deleted!"
                            st.session_state.show_success = True
                            st.rerun()
            
            st.divider()

    # Show edit dialog if triggered
    if st.session_state.show_edit_dialog and st.session_state.edit_debt_id:
        debt_to_edit = api_client.get_debt(st.session_state.edit_debt_id)
        if debt_to_edit:
            edit_debt_dialog(debt_to_edit)
        else:
            st.error("Debt not found.")
            st.session_state.edit_debt_id = None
            st.session_state.show_edit_dialog = False

    # Refresh button in sidebar
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()


if __name__ == "__main__":
    main()
