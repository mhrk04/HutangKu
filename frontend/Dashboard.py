"""
Dashboard Page - Main read-only overview
Displays KPIs, urgent notifications, and BNPL grouping
"""
import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
from collections import defaultdict
from requests.exceptions import RequestException

# Add parent directory to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from frontend.utils.api_client import APIClient

# Page configuration
st.set_page_config(
    page_title="Dashboard - HutangKu - Debt Management",
    page_icon="📊",
    layout="wide"
)

# Initialize API client
api_client = APIClient()

def calculate_days_until_due(due_date_str: str) -> int:
    """Calculate days until due date"""
    try:
        due_date = datetime.fromisoformat(due_date_str).date()
        today = datetime.now().date()
        return (due_date - today).days
    except (ValueError, TypeError):
        return 999  # Return large number if date parsing fails

def main():
    st.title("📊 Personal Debt Dashboard")
    st.markdown("---")
    
    # Fetch all debts
    try:
        all_debts = api_client.get_all_debts()
    except RequestException as e:
        st.error(f"Failed to connect to the API. Please ensure the backend is running. Error: {e}")
        return

    if not all_debts:
        st.info("No debts found. Go to 'Manage Debts' to add your first debt record.")
        return

    # --- Data Processing ---
    df = pd.DataFrame(all_debts)
    
    # Convert MongoDB ObjectId to string if present (fixes Arrow serialization)
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)
    
    # Ensure string columns are properly typed
    if 'company_name' in df.columns:
        df['company_name'] = df['company_name'].astype(str)
    if 'status' in df.columns:
        df['status'] = df['status'].astype(str)
    if 'notes' in df.columns:
        df['notes'] = df['notes'].fillna('').astype(str)
    
    # Convert dates properly
    df['due_date'] = pd.to_datetime(df['due_date'])
    
    # Clean monetary columns to ensure they are numeric
    for col in ['amount_owed', 'minimum_payment']:
        df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df['days_until_due'] = df['due_date'].apply(lambda x: (x.date() - datetime.now().date()).days if pd.notna(x) else 9999)
    
    active_debts_df = df[df['status'] == 'Active Debt'].copy()
    active_debts_df['is_overdue'] = active_debts_df['days_until_due'] < 0

    # === URGENT NOTIFICATIONS SECTION ===
    st.header("🚨 Urgent Notifications")
    
    overdue_debts_df = active_debts_df[active_debts_df['is_overdue']].sort_values('days_until_due')
    due_soon_df = active_debts_df[(active_debts_df['days_until_due'] >= 0) & (active_debts_df['days_until_due'] <= 7)].sort_values('days_until_due')

    if overdue_debts_df.empty and due_soon_df.empty:
        st.success("✅ No overdue debts or payments due in the next 7 days!")
    else:
        if not overdue_debts_df.empty:
            st.subheader("Overdue Payments")
            for _, debt in overdue_debts_df.iterrows():
                days_overdue = abs(debt['days_until_due'])
                st.error(f"**{debt['company_name']}** - **{days_overdue} day{'s' if days_overdue > 1 else ''} OVERDUE!** Amount: RM{debt['minimum_payment']:.2f}")
        
        if not due_soon_df.empty:
            st.subheader("Upcoming Payments")
            for _, debt in due_soon_df.iterrows():
                days = debt['days_until_due']
                if days == 0:
                    st.warning(f"**{debt['company_name']}** - Payment DUE TODAY! Amount: RM{debt['minimum_payment']:.2f}")
                elif days == 1:
                    st.warning(f"**{debt['company_name']}** - Payment due TOMORROW! Amount: RM{debt['minimum_payment']:.2f}")
                else:
                    st.warning(f"**{debt['company_name']}** - Payment due in {days} days! Amount: RM{debt['minimum_payment']:.2f}")
    
    st.markdown("---")

    # --- KPIs ---
    st.header("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    total_outstanding = active_debts_df['amount_owed'].sum()
    total_overdue = active_debts_df[active_debts_df['is_overdue']]['amount_owed'].sum()
    due_soon_count = active_debts_df[(active_debts_df['days_until_due'] >= 0) & (active_debts_df['days_until_due'] <= 7)].shape[0]
    overdue_count = active_debts_df[active_debts_df['is_overdue']].shape[0]

    col1.metric("Total Outstanding Debt", f"RM {total_outstanding:,.2f}")
    col2.metric("Total Overdue Debt", f"RM {total_overdue:,.2f}", delta=f"{overdue_count} debts", delta_color="inverse")
    col3.metric("Debts Due Soon (7 days)", f"{due_soon_count} debts")
    col4.metric("Settled Debts", f"{df[df['status'] == 'Paid Off'].shape[0]} debts")
    
    st.markdown("---")
    
    # --- Charts ---
    st.header("Visualizations")

    st.subheader("Debt Composition Treemap")
    # Prepare data for treemap by combining active, overdue, and paid-off debts
    if not df.empty:
        # Categorize active and overdue debts
        treemap_df_active = active_debts_df.copy()
        treemap_df_active['display_status'] = treemap_df_active.apply(lambda row: 'Overdue' if row['is_overdue'] else 'Active', axis=1)
        
        # Get paid-off debts
        treemap_df_paid = df[df['status'] == 'Paid Off'].copy()
        treemap_df_paid['display_status'] = 'Paid Off'
        
        # Combine all categories
        combined_treemap_df = pd.concat([treemap_df_active, treemap_df_paid])
        
        # A treemap can only visualize positive values, so we filter out any zero amounts
        combined_treemap_df = combined_treemap_df[combined_treemap_df['amount_owed'] > 0]
        
        if not combined_treemap_df.empty:
            # Aggregate by status + company so multiple entries for the same company are summed
            agg_df = (
                combined_treemap_df
                .groupby(['display_status', 'company_name'], as_index=False)
                .agg({'amount_owed': 'sum'})
            )
            agg_df['rm_text'] = agg_df['amount_owed'].apply(lambda x: f"RM {x:,.2f}")

            fig_treemap = px.treemap(
                agg_df,
                path=[px.Constant("All Debts"), 'display_status', 'company_name'],
                values='amount_owed',
                color='display_status',
                color_discrete_map={
                    'Active': "#f7db0c",
                    'Overdue': '#d62728',
                    'Paid Off': '#2ca02c'
                },
                title='Debt Composition by Status and Company',
                custom_data=['rm_text']
            )

            # Use the aggregated numeric %{value} for display so the summed company value appears
            fig_treemap.update_traces(
                textinfo='text',
                texttemplate='<b>%{label}</b><br>RM %{value:,.2f}',
                hovertemplate='<b>%{label}</b><br>Amount: %{customdata[0]}<br>Category: %{parent}<extra></extra>'
            )

            fig_treemap.update_layout(margin=dict(t=50, l=25, r=25, b=25))
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("No debts with a positive amount to visualize in the treemap.")
    else:
        st.info("No debt data available to build a treemap.")

    st.markdown("---")

    # Sidebar filters removed — treemap already handles status selection
    # Default to showing active debts in the company grouping section
    display_debts = [debt for debt in all_debts if debt['status'] == 'Active Debt']
    
    # === BNPL GROUPING SECTION ===
    st.header("🏢 Debts Grouped by Company")
    
    # Group debts by company
    company_groups = defaultdict(list)
    for debt in display_debts:
        company_groups[debt["company_name"]].append(debt)
    
    # Display each company group
    if not company_groups:
        st.info("No active debts to display.")

    for company_name in sorted(company_groups.keys()):
        company_debts = company_groups[company_name]
        total_company_debt = sum(debt["amount_owed"] for debt in company_debts)
        
        # Create expander for each company
        with st.expander(
            f"**{company_name}** - Total Debt: RM {total_company_debt:,.2f} ({len(company_debts)} plan{'s' if len(company_debts) > 1 else ''})",
            expanded=len(company_debts) <= 3
        ):
            # Prepare data for display
            for debt in company_debts:
                days_until_due = calculate_days_until_due(debt["due_date"])
                due_date_display = datetime.fromisoformat(debt["due_date"]).strftime("%d %b %Y")
                
                # Color code based on urgency
                if days_until_due >= 0 and days_until_due <= 7 and debt["status"] == "Active Debt":
                    st.markdown(f"🔴 **URGENT** - Due in {days_until_due} day{'s' if days_until_due != 1 else ''}")
                
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**Status:** {debt['status']}")
                    if debt.get('notes'):
                        st.caption(f"Notes: {debt['notes']}")
                
                with col2:
                    st.write("**Amount Owed:**")
                    st.write(f"RM {debt['amount_owed']:.2f}")
                
                with col3:
                    st.write("**Min. Payment:**")
                    st.write(f"RM {debt['minimum_payment']:.2f}")
                
                with col4:
                    st.write("**Due Date:**")
                    st.write(due_date_display)
                
                st.divider()
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

if __name__ == "__main__":
    main()
