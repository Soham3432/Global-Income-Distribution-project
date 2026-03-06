import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    layout="wide",
    page_title="Global Income Analytics Platform",
    page_icon="🌍"
)

# ================================
# ADVANCED UI STYLE (3D + GLASS)
# ================================
st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

/* Sidebar */

section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#141e30,#243b55);
border-right:1px solid rgba(255,255,255,0.1);
}

/* Cards */

.card{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(10px);
padding:25px;
border-radius:20px;
margin:10px;
box-shadow:0 10px 40px rgba(0,0,0,0.4);
transition:0.4s;
}

.card:hover{
transform: translateY(-10px) scale(1.03);
box-shadow:0 20px 60px rgba(0,0,0,0.6);
}

/* KPI tiles */

.metric-card{
background: linear-gradient(145deg,#1f4037,#99f2c8);
padding:20px;
border-radius:15px;
color:black;
font-weight:bold;
text-align:center;
font-size:18px;
box-shadow:0 10px 30px rgba(0,0,0,0.4);
transition:0.3s;
}

.metric-card:hover{
transform:scale(1.08);
}

/* Buttons */

.stButton>button{
background:linear-gradient(45deg,#ff512f,#dd2476);
color:white;
border-radius:10px;
border:none;
padding:10px 20px;
font-weight:bold;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.1);
}

/* Title */

h1{
text-shadow:0px 0px 15px rgba(0,255,255,0.7);
}

</style>
""", unsafe_allow_html=True)

# ================================
# LOGIN SYSTEM
# ================================

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

# ================================
# SIDEBAR
# ================================

st.sidebar.title("🌍 Global Income Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Summary",
        "Project Overview",
        "Data Collection",
        "Data Cleaning",
        "Data Modeling & DAX",
        "Dashboard",
        "Insights & Impact",
        "Feedback",
        "Admin Panel"
    ]
)

# ================================
# EXECUTIVE SUMMARY
# ================================

if page == "Executive Summary":

    st.title("🌍 Global Income Intelligence Platform")

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown('<div class="metric-card">📊 Countries<br><h2>165</h2></div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="metric-card">🌎 Regions<br><h2>7</h2></div>',unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="metric-card">📈 Avg Gini<br><h2>41.2</h2></div>',unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="metric-card">👥 Population<br><h2>6.8B</h2></div>',unsafe_allow_html=True)

    st.markdown("""
    <div class="card">

    <h3>📌 Project Mission</h3>

    This platform analyzes global income inequality trends using
    economic indicators such as **Gini Index**, **Palma Ratio**, and
    **population statistics**.

    The goal is to help policymakers, researchers, and analysts
    understand inequality patterns globally.

    </div>
    """, unsafe_allow_html=True)

# ================================
# PROJECT OVERVIEW
# ================================

elif page == "Project Overview":

    st.title("🚀 End-to-End Analytics Workflow")

    st.markdown("""
    <div class="card">

    🔹 Data Collection → Global inequality datasets  

    🔹 Data Cleaning → Power Query transformation  

    🔹 Data Modeling → Star schema relationships  

    🔹 DAX Measures → KPI calculations  

    🔹 Dashboard Design → Interactive visual analytics  

    🔹 Deployment → Web application using Streamlit  

    </div>
    """,unsafe_allow_html=True)

# ================================
# DATA COLLECTION
# ================================

elif page == "Data Collection":

    st.title("📥 Data Collection")

    st.markdown("""
    <div class="card">

    Dataset contains:

    • Country Name  
    • Year  
    • Gini Index  
    • Palma Ratio  
    • Income Share Distribution  
    • Total Population  
    • World Bank Region  

    Data Sources:
    - World Bank
    - Public inequality datasets

    </div>
    """,unsafe_allow_html=True)

# ================================
# DATA CLEANING
# ================================

elif page == "Data Cleaning":

    st.title("🧹 Data Cleaning & Transformation")

    st.markdown("""
    <div class="card">

    Steps performed in Power BI:

    • Removed null values  
    • Handled missing records  
    • Converted columns to numeric format  
    • Removed duplicates  
    • Standardized country names  
    • Created calculated columns  

    Derived Columns:

    - Income Category
    - Inequality Level

    </div>
    """,unsafe_allow_html=True)

# ================================
# DATA MODELING
# ================================

elif page == "Data Modeling & DAX":

    st.title("📊 Data Modeling & DAX")

    st.markdown("""
    <div class="card">

    Important DAX Measures:

    Total Population =
    SUM([Total_Population])

    Average Gini Index =
    AVERAGE([Gini_Index])

    Previous Year Inequality =
    CALCULATE(
        [Average Gini Index],
        PREVIOUSYEAR([Year])
    )

    Inequality Change % =
    DIVIDE(
        [Average Gini Index] -
        [Previous Year Inequality],
        [Previous Year Inequality]
    )

    </div>
    """,unsafe_allow_html=True)

# ================================
# DASHBOARD
# ================================

elif page == "Dashboard":

    st.title("📊 Interactive Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9" 

    st.components.v1.iframe(powerbi_url, width=1400, height=750)

# ================================
# INSIGHTS
# ================================

elif page == "Insights & Impact":

    st.title("📈 Key Insights")

    st.markdown("""
    <div class="card">

    Key Observations:

    • African regions show higher inequality levels.

    • Medium inequality category contains most countries.

    • Population-weighted inequality highlights economic
      concentration in developing economies.

    Business Impact:

    • Helps policymakers analyze inequality trends

    • Supports global economic planning

    • Enables cross-region comparison

    </div>
    """,unsafe_allow_html=True)

# ================================
# FEEDBACK
# ================================

elif page == "Feedback":

    st.title("💬 Community Feedback")

    with st.form("feedback_form"):

        name = st.text_input("Your Name")
        rating = st.slider("Project Rating ⭐",1,5)
        comments = st.text_area("Your Feedback")

        submitted = st.form_submit_button("Submit")

        if submitted:

            feedback_data = {
                "Name":name,
                "Rating":rating,
                "Comments":comments,
                "Date":datetime.now()
            }

            df = pd.DataFrame([feedback_data])

            if not os.path.isfile("feedback.csv"):
                df.to_csv("feedback.csv",index=False)
            else:
                df.to_csv("feedback.csv",mode="a",header=False,index=False)

            st.success("🎉 Feedback Submitted!")

# ================================
# ADMIN PANEL
# ================================

elif page == "Admin Panel":

    st.title("🛠 Admin Analytics")

    if os.path.isfile("feedback.csv"):

        df = pd.read_csv("feedback.csv")

        st.dataframe(df)

        st.metric(
            "Average Rating",
            round(df["Rating"].mean(),2)
        )

        st.bar_chart(df["Rating"].value_counts())

    else:
        st.warning("No feedback available.")

# ================================
# FOOTER
# ================================

st.markdown("""
<hr>

<center>

🌍 <b>Global Income Analytics Platform</b>

End-to-End Data Analytics Project

Built using Python • Power BI • Streamlit

</center>
""", unsafe_allow_html=True)