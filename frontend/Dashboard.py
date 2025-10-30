"""
Dashboard Page - Main read-only overview
Displays KPIs, urgent notifications, and visualizations
"""
import streamlit as st
import sys
import os
from datetime import datetime
import pandas as pd
import plotly.express as px
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
    # Handle both numeric and string types properly
    for col in ['amount_owed', 'minimum_payment']:
        if df[col].dtype == 'object':  # If string type
            df[col] = df[col].astype(str).str.replace(r'[^\d.]', '', regex=True)
            df[col] = pd.to_numeric(df[col], errors='coerce')
        else:  # If already numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')
        # Don't fillna - keep NaN as is for now, filter later if needed
        # Replace only actual NaN (missing data) with 0, not valid small numbers
        df[col] = df[col].fillna(0)

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
    st.header("📈 Debt Visualizations")
    
    if not df.empty:
        # Categorize active and overdue debts
        treemap_df_active = active_debts_df.copy()
        treemap_df_active['display_status'] = treemap_df_active.apply(lambda row: 'Overdue' if row['is_overdue'] else 'Active', axis=1)
        
        # Get paid-off debts
        treemap_df_paid = df[df['status'] == 'Paid Off'].copy()
        treemap_df_paid['display_status'] = 'Paid Off'
        
        # Combine all categories
        combined_treemap_df = pd.concat([treemap_df_active, treemap_df_paid])
        # Only filter out actual zeros and negative values, keep all positive values
        combined_treemap_df = combined_treemap_df[combined_treemap_df['amount_owed'] > 0]
        
        if not combined_treemap_df.empty:
            # Aggregate by status + company
            agg_df = (
                combined_treemap_df
                .groupby(['display_status', 'company_name'], as_index=False)
                .agg({'amount_owed': 'sum'})
            )
            
            # --- Group small debts for better visualization ---
            small_debt_threshold = 1.00
            large_debts = agg_df[agg_df['amount_owed'] >= small_debt_threshold].copy()
            small_debts = agg_df[agg_df['amount_owed'] < small_debt_threshold].copy()
            
            if not small_debts.empty:
                small_debts_summary = small_debts.groupby('display_status', as_index=False).agg(
                    amount_owed=('amount_owed', 'sum'),
                    count=('company_name', 'count')
                )
                small_debts_summary['company_name'] = small_debts_summary.apply(
                    lambda row: f"Other Debts (< RM {small_debt_threshold:.2f}) - {row['count']} items",
                    axis=1
                )
                final_agg_df = pd.concat([large_debts, small_debts_summary[['display_status', 'company_name', 'amount_owed']]])
            else:
                final_agg_df = large_debts
            
            if not small_debts.empty:
                st.info(f"💡 Note: {len(small_debts)} debt(s) with amounts less than RM {small_debt_threshold:.2f} have been grouped. See the full list on the 'Active Debts' page.")

            # === 1. DEBT BY STATUS - PIE CHART ===
            st.subheader("💰 Debt Distribution")
            status_df = final_agg_df.groupby('display_status', as_index=False).agg({'amount_owed': 'sum'})
            
            fig_pie = px.pie(
                status_df, values='amount_owed', names='display_status', color='display_status',
                color_discrete_map={'Active': "#f7db0c", 'Overdue': '#d62728', 'Paid Off': '#2ca02c'},
                hole=0.4
            )
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='label+percent',
                textfont_size=14,
                hovertemplate='<b>%{label}</b><br>Amount: RM %{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
            )
            fig_pie.update_layout(
                showlegend=True, 
                height=450, 
                margin=dict(t=20, l=10, r=10, b=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # === 2. TOP DEBTS BY COMPANY - BAR CHART ===
            st.subheader("🏢 Top Debts by Company")
            active_companies = final_agg_df[final_agg_df['display_status'].isin(['Active', 'Overdue'])].copy()
            
            if not active_companies.empty:
                top_companies = active_companies.nlargest(10, 'amount_owed')
                fig_bar = px.bar(
                    top_companies, y='company_name', x='amount_owed', color='display_status',
                    color_discrete_map={'Active': "#f7db0c", 'Overdue': '#d62728'},
                    orientation='h', text='amount_owed'
                )
                fig_bar.update_traces(
                    texttemplate='RM %{text:,.0f}', 
                    textposition='inside',
                    textfont=dict(size=11, color='black'),
                    insidetextanchor='end',
                    hovertemplate='<b>%{y}</b><br>Amount: RM %{x:,.2f}<br>Status: %{fullData.name}<extra></extra>'
                )
                fig_bar.update_layout(
                    xaxis_title="", 
                    yaxis_title="", 
                    showlegend=True,
                    height=max(350, len(top_companies) * 40), 
                    margin=dict(t=40, l=5, r=10, b=10),
                    yaxis={'categoryorder': 'total ascending'},
                    legend=dict(
                        title=dict(text="Status", font=dict(size=11)),
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="left",
                        x=0,
                        font=dict(size=10)
                    ),
                    xaxis=dict(visible=False)
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No active debts to display.")
            # === 3. PAYMENT URGENCY TIMELINE ===
            if not active_debts_df.empty:
                st.subheader("⏰ Payment Urgency Timeline")
                
                def categorize_urgency(days):
                    if days < 0: return "Overdue"
                    elif days == 0: return "Due Today"
                    elif days <= 3: return "1-3 days"
                    elif days <= 7: return "4-7 days"
                    elif days <= 14: return "8-14 days"
                    else: return ">14 days"
                
                active_debts_df['urgency'] = active_debts_df['days_until_due'].apply(categorize_urgency)
                urgency_summary = active_debts_df.groupby('urgency', as_index=False).agg(
                    total_amount=('amount_owed', 'sum'),
                    count=('company_name', 'count')
                )
                urgency_order = ["Overdue", "Due Today", "1-3 days", "4-7 days", "8-14 days", ">14 days"]
                urgency_summary['urgency'] = pd.Categorical(urgency_summary['urgency'], categories=urgency_order, ordered=True)
                urgency_summary = urgency_summary.sort_values('urgency')
                
                urgency_colors = {
                    "Overdue": '#d62728', "Due Today": '#ff7f0e', "1-3 days": '#ffbb00',
                    "4-7 days": '#f7db0c', "8-14 days": '#2ca02c', ">14 days": '#1f77b4'
                }
                
                fig_urgency = px.bar(
                    urgency_summary, x='urgency', y='total_amount', color='urgency',
                    color_discrete_map=urgency_colors, text='count'
                )
                fig_urgency.update_traces(
                    texttemplate='%{text} debt(s)<br>RM %{y:,.0f}', 
                    textposition='outside',
                    textfont_size=11,
                    hovertemplate='<b>%{x}</b><br>Total Amount: RM %{y:,.2f}<br>Number of Debts: %{text}<extra></extra>'
                )
                fig_urgency.update_layout(
                    xaxis_title="", 
                    yaxis_title="Total Amount (RM)",
                    showlegend=False, 
                    height=400, 
                    margin=dict(t=20, l=10, r=10, b=80),
                    xaxis_tickangle=-45,
                    xaxis=dict(tickfont=dict(size=11))
                )
                st.plotly_chart(fig_urgency, use_container_width=True)

            # --- Debt Composition Treemap (full width) ---
            st.subheader("🗺️ Detailed Debt Composition")
            
            def format_amount(amount):
                if amount >= 1000: return f"RM {amount:,.0f}"
                elif amount >= 1: return f"RM {amount:.2f}"
                else: return f"RM {amount:.4f}"
            
            final_agg_df['rm_text'] = final_agg_df['amount_owed'].apply(format_amount)
            
            fig_treemap = px.treemap(
                final_agg_df,
                path=[px.Constant("All Debts"), 'display_status', 'company_name'],
                values='amount_owed', color='display_status',
                color_discrete_map={'Active': "#f7db0c", 'Overdue': '#d62728', 'Paid Off': '#2ca02c'},
                custom_data=['rm_text']
            )
            fig_treemap.update_traces(
                textposition='middle center',
                texttemplate='%{label}<br>%{customdata[0]}',
                hovertemplate='<b>%{label}</b><br>Amount: %{customdata[0]}<br>Category: %{parent}<extra></extra>',
                marker=dict(line=dict(width=2, color='white')),
                textfont=dict(size=12)
            )
            fig_treemap.update_layout(
                height=500, 
                margin=dict(t=20, l=5, r=5, b=5),
                uniformtext=dict(minsize=9, mode='hide')
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("No debts with a positive amount to visualize.")
    else:
        st.info("No debt data available to build visualizations.")

    st.markdown("---")
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()

if __name__ == "__main__":
    main()
