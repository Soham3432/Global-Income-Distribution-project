import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide", page_title="Global Income Analytics Platform", page_icon="🌍")

# =============================
# LOGIN SYSTEM
# =============================
def login():
    st.title("🔐 Global Income Analytics Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful!")
        else:
            st.error("Invalid Credentials")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# =============================
# SIDEBAR NAVIGATION
# =============================
st.sidebar.title("🌍 Global Income Analytics")
page = st.sidebar.radio("Navigation", [
    "Executive Summary",
    "Project Overview",
    "Data Collection",
    "Data Cleaning",
    "Data Modeling & DAX",
    "Dashboard",
    "Insights & Impact",
    "Feedback",
    "Admin Panel"
])

# =============================
# EXECUTIVE SUMMARY
# =============================
if page == "Executive Summary":
    st.title("📌 Executive Summary")

    st.markdown("""
    This project analyzes global income inequality using population and income distribution data.

    Objectives:
    - Understand income disparities across regions
    - Analyze Gini Index trends over time
    - Identify high inequality countries
    - Study relationship between population & inequality

    Tools Used:
    - Power BI (Visualization & DAX)
    - Python (Streamlit Deployment)
    """)

# =============================
# PROJECT OVERVIEW
# =============================
elif page == "Project Overview":
    st.title("📖 Project Overview")

    st.markdown("""
    Problem Statement:
    Income inequality remains a global economic concern. This project aims to visualize
    income distribution patterns and identify key inequality trends.

    Approach:
    1. Data Collection
    2. Data Cleaning & Transformation
    3. Data Modeling
    4. DAX Measure Creation
    5. Dashboard Development
    6. Web Deployment using Streamlit
    """)

# =============================
# DATA COLLECTION
# =============================
elif page == "Data Collection":
    st.title("📥 Data Collection")

    st.write("""
    Dataset includes:
    - Country
    - Year
    - Gini Index
    - Palma Ratio
    - Income Share Data
    - Total Population
    - World Bank Region

    Source: Global income distribution datasets (World Bank / public datasets)
    """)

# =============================
# DATA CLEANING
# =============================
elif page == "Data Cleaning":
    st.title("🧹 Data Cleaning & Transformation")

    st.markdown("""
    Steps Performed in Power BI:

    - Removed blank values
    - Filled missing data
    - Converted text columns to numeric
    - Extracted Year from date columns
    - Created calculated columns:
        - Income Category
        - Inequality Category
    - Removed duplicates
    - Standardized country names
    """)

# =============================
# DATA MODELING & DAX
# =============================
elif page == "Data Modeling & DAX":
    st.title("📊 Data Modeling & DAX Measures")

    st.markdown("""
    Important Measures Created:

    Total Population =
    SUM([Total_Population])

    Average Gini Index =
    AVERAGE([Gini_Index])

    Previous Year Inequality =
    CALCULATE([Average Gini Index], PREVIOUSYEAR([Year]))

    Inequality Change % =
    DIVIDE([Average Gini Index] - [Previous Year Inequality],
           [Previous Year Inequality])
    """)

# =============================
# DASHBOARD SECTION
# =============================
elif page == "Dashboard":
    st.title("📊 Power BI Interactive Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9" 
    st.components.v1.iframe(powerbi_url, width=1400, height=750)

# =============================
# INSIGHTS & BUSINESS IMPACT
# =============================
elif page == "Insights & Impact":
    st.title("📈 Key Insights & Business Impact")

    st.markdown("""
    Key Insights:
    - Certain regions consistently show higher inequality.
    - Population-weighted inequality highlights economic concentration.
    - Medium inequality category contains majority of countries.

    Business Impact:
    - Helps policymakers understand inequality distribution.
    - Supports data-driven economic planning.
    - Enables comparative regional analysis.
    """)

# =============================
# FEEDBACK SYSTEM
# =============================
elif page == "Feedback":
    st.title("💬 Share Your Feedback")

    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        rating = st.slider("Rate this Project (1-5)", 1, 5)
        comments = st.text_area("Your Feedback")

        submitted = st.form_submit_button("Submit")

        if submitted:
            feedback_data = {
                "Name": name,
                "Rating": rating,
                "Comments": comments,
                "Date": datetime.now()
            }

            df = pd.DataFrame([feedback_data])

            if not os.path.isfile("feedback.csv"):
                df.to_csv("feedback.csv", index=False)
            else:
                df.to_csv("feedback.csv", mode="a", header=False, index=False)

            st.success("✅ Thank you for your feedback!")

# =============================
# ADMIN PANEL
# =============================
elif page == "Admin Panel":
    st.title("🛠 Admin Analytics Panel")

    if os.path.isfile("feedback.csv"):
        df = pd.read_csv("feedback.csv")

        st.subheader("All Feedback")
        st.dataframe(df)

        st.metric("Average Rating", round(df["Rating"].mean(), 2))

        st.bar_chart(df["Rating"].value_counts())
    else:
        st.warning("No feedback data yet.")

# =============================
# FOOTER
# =============================
st.markdown("---")
st.markdown("© 2026 Global Income Analytics Platform | End-to-End Data Analytics Project")