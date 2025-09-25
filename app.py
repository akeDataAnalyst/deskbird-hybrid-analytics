#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np
import os
from dotenv import load_dotenv

# 1. CONFIGURATION AND UTILITIES 

# Load environment variables
load_dotenv()

#  Database Connection
@st.cache_resource
def get_db_connection():
    """Establishes and caches the database connection."""
    try:
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')

        if not all([db_user, db_password, db_host, db_name]):
            st.error("Database credentials not found. Check your .env file.")
            return None

        connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Utility function to run SQL
@st.cache_data
def run_sql(query):
    """Runs a SQL query and returns a DataFrame."""
    engine = get_db_connection()
    if engine:
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn)
        return df
    return pd.DataFrame()

#  2. ANALYTICAL QUERIES (Same as before)

@st.cache_data
def get_funnel_data():
    """Queries Growth Funnel Metrics for the Executive Summary."""
    query = """
    SELECT
        company_size,
        SUM(total_leads) AS "Total Leads",
        SUM(total_customers) AS "Total Customers",
        SUM(total_revenue) AS "Total Revenue",
        (SUM(total_customers) * 100.0) / NULLIF(SUM(total_leads), 0) AS "Conversion Rate (%)"
    FROM
        growth_funnel_mart
    GROUP BY 1
    ORDER BY "Conversion Rate (%)" DESC;
    """
    df = run_sql(query)
    df['Total Revenue'] = df['Total Revenue'].map('${:,.2f}'.format)
    df['Conversion Rate (%)'] = df['Conversion Rate (%)'].map('{:.2f}%'.format)
    return df

@st.cache_data
def get_utilization_data():
    """Queries Office Utilization by Day and Segment."""
    query = """
    SELECT
        CASE day_of_week
            WHEN 1 THEN 'Sunday'
            WHEN 2 THEN 'Monday'
            WHEN 3 THEN 'Tuesday'
            WHEN 4 THEN 'Wednesday'
            WHEN 5 THEN 'Thursday'
            WHEN 6 THEN 'Friday'
            WHEN 7 THEN 'Saturday'
        END AS "Day of Week",
        company_size AS "Segment",
        SUM(total_desk_bookings) AS "Desk Bookings",
        SUM(total_room_bookings) AS "Room Bookings"
    FROM
        office_utilization_mart
    GROUP BY 1, 2
    ORDER BY "Desk Bookings" DESC;
    """
    return run_sql(query)

@st.cache_data
def get_propensity_results():
    """Simulates loading the final, analyzed Odds Ratios."""
    data = {
        'Segment': ['Enterprise (Baseline)', 'Mid-Market', 'SMB'],
        'Odds Ratio': [1.0, 0.277, 0.189],
        'Likelihood Comparison (vs. Enterprise)': ['1.0x (Baseline)', '72.3% Lower', '81.1% Lower']
    }
    df = pd.DataFrame(data)
    return df

#  3. STREAMLIT APP LAYOUT

def main():
    st.set_page_config(layout="wide", page_title="Deskbird Workplace Intelligence Dashboard")

    # Catchy new title focused on the core product area
    st.title("🦅 Deskbird Hybrid Workplace Intelligence")
    st.subheader("Data-Driven Strategies for Revenue Growth & Office Optimization")
    st.markdown("---")

    # Load all data upfront
    funnel_df = get_funnel_data()
    propensity_df = get_propensity_results()
    util_df = get_utilization_data()

    if funnel_df.empty:
        st.error("Data loading failed. Please check database connection.")
        return

    # TOP METRICS (Button/Card Style) 
    st.header("I. Executive Metrics Snapshot")

    col1, col2, col3 = st.columns(3)

    # 1. Highest Converting Segment
    col1.metric("Highest Conversion Rate 📈", "35.90%", "Enterprise")
    col1.caption("Indicates best product-market fit post-lead qualification.")

    # 2. Highest Value Segment
    adv_mm = '${:,.0f}'.format(95725.42 / 9.0) 
    col2.metric("Highest Deal Value (ADV) 💰", adv_mm, "Mid-Market")
    col2.caption("Highest revenue per customer, but requires optimization.")

    # 3. Model Priority
    col3.metric("Highest Propensity to Close ⭐", "72% Higher Odds", "Enterprise")
    col3.caption("Based on Logistic Regression Model Odds Ratios.")

    st.markdown("---")

    # ANALYSIS SECTIONS (Using Tabs for Clean Navigation)

    # Order changed to Propensity first (highest ROI action), then Funnel, then Utilization
    tab1, tab2, tab3 = st.tabs([
        "⭐ Sales Prioritization (Propensity)",
        "📈 Funnel Conversion Deep Dive",
        "🏢 Utilization & Workplace Insights"
    ])

    # --- TAB 1: PROPENSITY MODELING ---
    with tab1:
        st.header("Sales Prioritization: Propensity to Convert")
        st.markdown("""
        The Logistic Regression Model identifies segments that are most likely to convert after becoming a qualified lead. **Enterprise** is the baseline for comparison.
        """)

        st.dataframe(propensity_df, use_container_width=True, hide_index=True)

        st.subheader("Actionable Takeaways")
        st.success("""
        **1. Model-Driven Focus:** Enterprise leads must receive immediate, high-touch sales attention, as they are the only segment with a high statistical probability of closing.

        **2. Mid-Market Diagnostic:** Launch an investigation into why Mid-Market, despite its high ADV, has a 72% lower conversion probability. There is a systemic bottleneck preventing high-value deals from closing.
        """)

    # --- TAB 2: FUNNEL CONVERSION DEEP DIVE ---
    with tab2:
        st.header("Segment-Level Funnel Performance")
        st.markdown("""
        This table breaks down lead volume, revenue, and conversion rates, revealing the trade-offs between volume and efficiency across market segments.
        """)

        st.dataframe(funnel_df, use_container_width=True, hide_index=True)

        st.subheader("Actionable Takeaways")
        st.warning("""
        **1. Optimize Mid-Market Funnel:** The highest ADV means every conversion lift here yields maximum return. Focus on closing the 18% conversion gap with Enterprise.

        **2. Re-evaluate SMB Strategy:** The lowest conversion rate (13.27%) coupled with low propensity (81% less likely to close) necessitates moving SMB leads to a **self-service or automated nurture track** to reduce inefficient sales spend.
        """)

    # --- TAB 3: UTILIZATION & WORKPLACE INSIGHTS ---
    with tab3:
        st.header("Client Workplace Utilization Patterns")
        st.markdown("""
        This analysis identifies peak days and segment-specific usage habits, essential for advising clients on real estate and energy optimization.
        """)

        st.dataframe(util_df.head(10), use_container_width=True, hide_index=True)

        st.subheader("Actionable Takeaways")
        st.info("""
        **1. Utilization Advisory Service:** Create a new consulting service based on non-traditional usage patterns (e.g., Enterprise weekend peaks, SMB high room-to-desk ratios).

        **2. Product Feature Focus:** Use the SMB data (high room demand on Mondays) to prioritize product features that make booking and managing collaboration spaces easier and more efficient.
        """)

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




