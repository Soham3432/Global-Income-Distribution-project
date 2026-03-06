import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(layout="wide", page_title="Global Income Analytics", page_icon="🌍")

# =========================
# SIMPLE LOGIN SYSTEM
# =========================
def login():
    st.title("🔐 Login to Dashboard")

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

# =========================
# SIDEBAR NAVIGATION
# =========================
st.sidebar.title("🌍 Global Income Analytics")
page = st.sidebar.radio("Navigation", 
                        ["Dashboard", "Project Info", "Feedback", "Admin Panel"])

# =========================
# DASHBOARD PAGE
# =========================
if page == "Dashboard":

    st.title("📊 Global Income Distribution Dashboard")
    st.markdown("Analyze global inequality trends and population distribution.")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9" 

    st.components.v1.iframe(powerbi_url, width=1400, height=750)

    st.markdown("### 📌 Key Insights")
    st.info("""
    - Income inequality varies significantly across regions.
    - High Gini Index countries dominate certain regions.
    - Population concentration impacts inequality trends.
    """)

# =========================
# PROJECT INFO PAGE
# =========================
elif page == "Project Info":

    st.title("📖 Project Overview")

    st.write("""
    This project analyzes global income distribution using:
    - Power BI for Data Visualization
    - DAX Measures & Calculated Columns
    - Streamlit for Web Deployment
    """)

    st.success("Tools Used: Power BI, Python, Streamlit")

# =========================
# FEEDBACK PAGE
# =========================
elif page == "Feedback":

    st.title("💬 Share Your Feedback")

    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        rating = st.slider("Rate this Dashboard (1-5)", 1, 5)
        comments = st.text_area("Your Feedback")

        submitted = st.form_submit_button("Submit")

        if submitted:
            feedback_data = {
                "Name": name,
                "Email": email,
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

# =========================
# ADMIN PANEL PAGE
# =========================
elif page == "Admin Panel":

    st.title("🛠 Admin Feedback Dashboard")

    if os.path.isfile("feedback.csv"):
        df = pd.read_csv("feedback.csv")

        st.subheader("📄 All Feedback")
        st.dataframe(df)

        st.subheader("⭐ Average Rating")
        st.metric("Avg Rating", round(df["Rating"].mean(), 2))

        st.subheader("📊 Rating Distribution")
        rating_counts = df["Rating"].value_counts().sort_index()
        st.bar_chart(rating_counts)

    else:
        st.warning("No feedback data available yet.")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("© 2026 Global Income Analytics | Built with Power BI & Streamlit")