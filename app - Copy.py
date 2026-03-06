import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =================================
# PAGE CONFIG
# =================================

st.set_page_config(
    page_title="Global Income Distribution Analytics",
    page_icon="🌍",
    layout="wide"
)

# =================================
# DARK PURPLE UI STYLE
# =================================

st.markdown("""
<style>

body{
background:linear-gradient(135deg,#14001f,#2c0054,#4b0082);
color:white;
}

.stApp{
background:linear-gradient(135deg,#14001f,#2c0054,#4b0082);
}

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#1a0033,#3a0066);
}

.kpi{
background:linear-gradient(145deg,#8e2de2,#4a00e0);
padding:25px;
border-radius:15px;
text-align:center;
font-weight:bold;
box-shadow:0px 10px 30px rgba(0,0,0,0.5);
margin-bottom:20px;
}

.glass{
background:rgba(255,255,255,0.05);
backdrop-filter:blur(12px);
padding:30px;
border-radius:15px;
box-shadow:0px 10px 40px rgba(0,0,0,0.6);
margin-bottom:25px;
}

h1{
text-shadow:0px 0px 20px rgba(200,0,255,0.8);
}

</style>
""", unsafe_allow_html=True)

# =================================
# LOGIN SYSTEM
# =================================

def login():

    st.title("🌍 Global Income Distribution Analytics Platform")

    st.markdown("### Secure Login")

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
# LOAD DATASET
# =================================

data_path = "final_dataset.csv"

if os.path.exists(data_path):

    df = pd.read_csv(data_path)

    # clean column names
    df.columns = df.columns.str.strip().str.replace(" ", "_")

else:

    df = pd.DataFrame()

# =================================
# SIDEBAR NAVIGATION
# =================================

st.sidebar.title("🌍 Analytics Platform")

page = st.sidebar.radio(
"Navigation",
[
"Home",
"Project Overview",
"Data Pipeline",
"Data Modeling",
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

    st.title("Global Income Distribution Analytics")

    st.markdown("""
    <div class="glass">

    This platform analyzes **global income inequality trends** using population
    and income distribution indicators.

    Key metrics analyzed:

    • Gini Index  
    • Palma Ratio  
    • Income distribution  
    • Population statistics  

    Built using **Power BI + Streamlit**

    </div>
    """, unsafe_allow_html=True)

    if not df.empty:

        total_population = int(df["Total_Population"].sum())
        avg_gini = round(df["Gini_Index"].mean(),2)
        countries = df["Country"].nunique()
        years = df["Year"].nunique()

    else:

        total_population = "-"
        avg_gini = "-"
        countries = "-"
        years = "-"

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="kpi">Total Population<br><h2>{total_population}</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="kpi">Average Gini Index<br><h2>{avg_gini}</h2></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="kpi">Countries Analyzed<br><h2>{countries}</h2></div>', unsafe_allow_html=True)

    with col4:
        st.markdown(f'<div class="kpi">Years Covered<br><h2>{years}</h2></div>', unsafe_allow_html=True)

# =================================
# PROJECT OVERVIEW
# =================================

elif page == "Project Overview":

    st.title("📊 Project Overview")

    st.markdown("""
    <div class="glass">

    Income inequality remains one of the most critical economic challenges globally.

    This project analyzes inequality patterns using data analytics
    and visualization techniques.

    **Objectives**

    • Understand income disparities across regions  
    • Identify countries with highest inequality  
    • Analyze trends across years  
    • Visualize population-weighted inequality  

    **Technology Stack**

    • Power BI – Data visualization  
    • Python – Backend analytics  
    • Streamlit – Web application  

    </div>
    """, unsafe_allow_html=True)

# =================================
# DATA PIPELINE
# =================================

elif page == "Data Pipeline":

    st.title("🔄 Data Pipeline")

    st.markdown("""
    <div class="glass">

    Dataset fields include:

    • Country  
    • Year  
    • Gini Index  
    • Palma Ratio  
    • Total Population  
    • World Bank Region  

    **Cleaning Steps**

    • Removed missing values  
    • Converted data types  
    • Standardized country names  
    • Removed duplicates  
    • Created calculated columns  

    </div>
    """, unsafe_allow_html=True)

# =================================
# DATA MODELING
# =================================

elif page == "Data Modeling":

    st.title("📈 Power BI Data Modeling")

    st.code("""

Total Updated Population =
SUM(Total_Population)

Average Gini Index =
AVERAGE(Gini_Index)

Previous Year Inequality =
CALCULATE(
[Average Gini Index],
PREVIOUSYEAR(Year)
)

Inequality Change % =
DIVIDE(
[Average Gini Index] - [Previous Year Inequality],
[Previous Year Inequality]
)

""")

# =================================
# DASHBOARD
# =================================

elif page == "Dashboard":

    st.title("📊 Interactive Power BI Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,width=1400,height=750)

# =================================
# INSIGHTS
# =================================

elif page == "Insights":

    st.title("📊 Key Insights")

    st.markdown("""
    <div class="glass">

    Major insights from the analysis:

    • Several countries in Africa show higher inequality levels  
    • Majority of countries fall into medium inequality category  
    • Population-weighted inequality highlights economic concentration  
    • Developed regions show relatively stable inequality trends  

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
        st.write("It compares income share of richest 10% with poorest 40%.")

    with st.expander("Why is income inequality important?"):
        st.write("High inequality can affect economic growth and social stability.")

# =================================
# FEEDBACK
# =================================

elif page == "Feedback":

    st.title("💬 Share Your Feedback")

    with st.form("feedback_form"):

        name = st.text_input("Your Name")
        rating = st.slider("Rate this project",1,5)
        comment = st.text_area("Comments")

        submit = st.form_submit_button("Submit")

        if submit:

            data = {
            "Name":name,
            "Rating":rating,
            "Comment":comment,
            "Date":datetime.now()
            }

            df_new = pd.DataFrame([data])

            if not os.path.isfile("feedback.csv"):
                df_new.to_csv("feedback.csv",index=False)
            else:
                df_new.to_csv("feedback.csv",mode="a",header=False,index=False)

            st.success("Thank you for your feedback!")

# =================================
# ADMIN PANEL
# =================================

elif page == "Admin Panel":

    st.title("🛠 Admin Panel")

    if os.path.exists("feedback.csv"):

        df_feedback = pd.read_csv("feedback.csv")

        st.dataframe(df_feedback)

        st.metric("Average Rating",round(df_feedback["Rating"].mean(),2))

        st.bar_chart(df_feedback["Rating"].value_counts())

    else:

        st.warning("No feedback data yet")

# =================================
# FOOTER
# =================================

st.markdown("""
---
<center>

Global Income Distribution Analytics Platform  
End-to-End Data Analytics Project  

Built with Power BI • Python • Streamlit

</center>
""", unsafe_allow_html=True)
