import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =================================
# PAGE CONFIG
# =================================

st.set_page_config(
    page_title="Global Income Analytics Platform",
    layout="wide",
    page_icon="🌍"
)

# =================================
# ADVANCED UI DESIGN
# =================================

st.markdown("""
<style>

body {
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

.stApp{
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#141e30,#243b55);
border-right:1px solid rgba(255,255,255,0.1);
}

/* GLASS CARD */

.glass{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(12px);
padding:30px;
border-radius:20px;
box-shadow:0px 10px 40px rgba(0,0,0,0.4);
margin-bottom:20px;
}

/* KPI CARD */

.kpi{
background: linear-gradient(145deg,#1f4037,#99f2c8);
padding:20px;
border-radius:15px;
color:black;
text-align:center;
font-weight:bold;
box-shadow:0 10px 30px rgba(0,0,0,0.5);
transition:0.3s;
}

.kpi:hover{
transform:scale(1.07);
}

/* TITLE */

h1{
text-shadow:0px 0px 20px rgba(0,255,255,0.8);
}

</style>
""", unsafe_allow_html=True)

# =================================
# LOGIN SYSTEM
# =================================

def login():

    st.title("🔐 Global Income Analytics Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True
            st.success("Login Successful")

        else:
            st.error("Invalid Credentials")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# =================================
# SIDEBAR NAVIGATION
# =================================

st.sidebar.title("🌍 Global Income Platform")

page = st.sidebar.radio(
"Navigation",
[
"Home",
"Executive Summary",
"Project Architecture",
"Data Pipeline",
"Data Modeling & DAX",
"Dashboard",
"Insights",
"FAQ",
"Feedback",
"Admin Panel"
]
)

# =================================
# HOME PAGE
# =================================

if page == "Home":

    st.title("🌍 Global Income Analytics Platform")

    st.markdown("""
    <div class="glass">

    This platform provides deep analysis of **global income inequality**  
    using population statistics and economic indicators.

    The system integrates:

    ✔ Data Analytics  
    ✔ Interactive Dashboards  
    ✔ Economic Insights  
    ✔ Public Feedback

    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown('<div class="kpi">Countries<br><h2>165</h2></div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="kpi">Regions<br><h2>7</h2></div>',unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="kpi">Avg Gini Index<br><h2>41.2</h2></div>',unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="kpi">Population<br><h2>6.8B</h2></div>',unsafe_allow_html=True)

# =================================
# EXECUTIVE SUMMARY
# =================================

elif page == "Executive Summary":

    st.title("📌 Executive Summary")

    st.markdown("""
    <div class="glass">

    Global income inequality remains one of the most significant
    economic challenges worldwide.

    This project explores inequality trends using indicators such as:

    • **Gini Index**  
    • **Palma Ratio**  
    • **Population Distribution**  
    • **Regional Income Share**

    The dashboard allows policymakers and researchers
    to analyze inequality trends across countries and regions.

    </div>
    """, unsafe_allow_html=True)

# =================================
# PROJECT ARCHITECTURE
# =================================

elif page == "Project Architecture":

    st.title("🏗 Project Architecture")

    st.markdown("""
    <div class="glass">

    End-to-End Data Analytics Architecture

    1️⃣ Data Collection  
    Global income datasets collected from public sources.

    2️⃣ Data Processing  
    Cleaning and transformation using Power Query.

    3️⃣ Data Modeling  
    Star schema structure with fact and dimension tables.

    4️⃣ Analytical Layer  
    KPI measures using DAX calculations.

    5️⃣ Visualization  
    Interactive dashboards built in Power BI.

    6️⃣ Deployment  
    Web application built using Streamlit.

    </div>
    """, unsafe_allow_html=True)

# =================================
# DATA PIPELINE
# =================================

elif page == "Data Pipeline":

    st.title("🔄 Data Pipeline")

    st.markdown("""
    <div class="glass">

    Dataset Fields:

    • Country  
    • Year  
    • Gini Index  
    • Palma Ratio  
    • Income Share  
    • Population  
    • Region

    Data Preparation Steps:

    - Removed null records  
    - Handled missing data  
    - Standardized country names  
    - Converted data types  
    - Created derived columns

    </div>
    """, unsafe_allow_html=True)

# =================================
# DATA MODELING
# =================================

elif page == "Data Modeling & DAX":

    st.title("📊 Data Modeling & DAX Measures")

    st.code("""

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

""")

# =================================
# DASHBOARD
# =================================

elif page == "Dashboard":

    st.title("📊 Interactive Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,width=1400,height=750)

# =================================
# INSIGHTS
# =================================

elif page == "Insights":

    st.title("📈 Key Insights")

    st.markdown("""
    <div class="glass">

    • Africa shows highest inequality in several years.

    • Medium inequality countries dominate global distribution.

    • Population-weighted inequality highlights economic concentration.

    • Some developed economies show stable inequality trends.

    </div>
    """, unsafe_allow_html=True)

# =================================
# FAQ
# =================================

elif page == "FAQ":

    st.title("❓ Frequently Asked Questions")

    with st.expander("What is the Gini Index?"):
        st.write("The Gini Index measures income inequality within a country.")

    with st.expander("What does Palma Ratio measure?"):
        st.write("It compares the richest 10% income share with poorest 40%.")

    with st.expander("Why is income inequality important?"):
        st.write("High inequality affects economic growth and social stability.")

    with st.expander("What tools were used in this project?"):
        st.write("Power BI, Python, Streamlit, and data analytics techniques.")

# =================================
# FEEDBACK
# =================================

elif page == "Feedback":

    st.title("💬 Share Your Feedback")

    with st.form("feedback_form"):

        name = st.text_input("Name")

        rating = st.slider("Rate this platform",1,5)

        comment = st.text_area("Comments")

        submit = st.form_submit_button("Submit")

        if submit:

            data = {
            "Name":name,
            "Rating":rating,
            "Comment":comment,
            "Date":datetime.now()
            }

            df = pd.DataFrame([data])

            if not os.path.isfile("feedback.csv"):
                df.to_csv("feedback.csv",index=False)
            else:
                df.to_csv("feedback.csv",mode="a",header=False,index=False)

            st.success("Feedback Submitted!")

# =================================
# ADMIN PANEL
# =================================

elif page == "Admin Panel":

    st.title("🛠 Admin Analytics")

    if os.path.exists("feedback.csv"):

        df = pd.read_csv("feedback.csv")

        st.dataframe(df)

        st.metric("Average Rating",round(df["Rating"].mean(),2))

        st.bar_chart(df["Rating"].value_counts())

    else:
        st.warning("No feedback available")

# =================================
# FOOTER
# =================================

st.markdown("""
---
<center>

🌍 Global Income Analytics Platform  
End-to-End Data Analytics Project

Built with Python • Power BI • Streamlit

</center>
""",unsafe_allow_html=True)