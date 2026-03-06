import streamlit as st
import pandas as pd
from datetime import datetime
import os

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Global Income Distribution Analytics",
    layout="wide",
    page_icon="🌍"
)

# ==================================
# DARK PURPLE UI STYLE
# ==================================

st.markdown("""
<style>

body {
background: linear-gradient(135deg,#14001f,#2a004f,#4b0082);
color:white;
}

.stApp{
background: linear-gradient(135deg,#14001f,#2a004f,#4b0082);
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#1b0033,#3b0066);
border-right:1px solid rgba(255,255,255,0.1);
}

/* GLASS CARD */

.glass{
background: rgba(255,255,255,0.05);
backdrop-filter: blur(12px);
padding:30px;
border-radius:18px;
box-shadow:0px 10px 40px rgba(0,0,0,0.5);
margin-bottom:20px;
}

/* KPI CARD */

.kpi{
background: linear-gradient(145deg,#7f00ff,#e100ff);
padding:20px;
border-radius:15px;
color:white;
text-align:center;
font-weight:bold;
box-shadow:0 10px 30px rgba(0,0,0,0.6);
transition:0.3s;
}

.kpi:hover{
transform:scale(1.06);
}

/* TITLE GLOW */

h1{
text-shadow:0px 0px 25px rgba(200,0,255,0.8);
}

</style>
""", unsafe_allow_html=True)

# ==================================
# LOGIN SYSTEM
# ==================================

def login():

    st.title("🌍 Global Income Distribution Analytics")

    st.markdown("### Secure Project Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("Login Successful")

        else:
            st.error("Invalid credentials")


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ==================================
# LOAD DATA (OPTIONAL)
# ==================================

data_path = "final.sheet.xlsx"

if os.path.exists(data_path):
    df = pd.read_excel(data_path)
else:
    df = pd.DataFrame()

# ==================================
# SIDEBAR NAVIGATION
# ==================================

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

# ==================================
# HOME PAGE
# ==================================

if page == "Home":

    st.title("Global Income Distribution Analytics Platform")

    st.markdown("""
    <div class="glass">

    This project analyzes **global income inequality trends**
    using economic indicators such as:

    • Gini Index  
    • Palma Ratio  
    • Income Distribution  
    • Population statistics  

    Built using Power BI and deployed through Streamlit.

    </div>
    """, unsafe_allow_html=True)

    if not df.empty:

        total_population = df["Total_Population"].sum()
        avg_gini = df["Gini_Index"].mean()
        countries = df["Country"].nunique()
        years = df["Year"].nunique()

    else:

        total_population = "Dataset Required"
        avg_gini = "-"
        countries = "-"
        years = "-"

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="kpi">Total Population<br><h2>{total_population}</h2></div>',unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="kpi">Average Gini Index<br><h2>{avg_gini}</h2></div>',unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="kpi">Countries Analyzed<br><h2>{countries}</h2></div>',unsafe_allow_html=True)

    with col4:
        st.markdown(f'<div class="kpi">Years Covered<br><h2>{years}</h2></div>',unsafe_allow_html=True)

# ==================================
# PROJECT OVERVIEW
# ==================================

elif page == "Project Overview":

    st.title("📊 Project Overview")

    st.markdown("""
    <div class="glass">

    Income inequality remains a major global challenge.
    This project analyzes inequality patterns using data analytics.

    **Objectives**

    • Identify countries with highest inequality  
    • Analyze inequality trends across years  
    • Compare regional income distribution  
    • Visualize population-weighted inequality  

    **Technology Stack**

    • Power BI – Dashboard visualization  
    • Python – Web application  
    • Streamlit – Interactive interface  

    </div>
    """, unsafe_allow_html=True)

# ==================================
# DATA PIPELINE
# ==================================

elif page == "Data Pipeline":

    st.title("🔄 Data Pipeline")

    st.markdown("""
    <div class="glass">

    Data fields used in analysis:

    • Country  
    • Year  
    • Gini Index  
    • Palma Ratio  
    • Total Population  
    • World Bank Region  

    **Data Cleaning Steps**

    • Missing value handling  
    • Data type correction  
    • Removing duplicates  
    • Creating calculated columns  

    </div>
    """, unsafe_allow_html=True)

# ==================================
# DATA MODELING
# ==================================

elif page == "Data Modeling":

    st.title("📈 Data Modeling & DAX")

    st.code("""

Total Updated Population =
SUM(Total_Population)

Avg Gini Index =
AVERAGE(Gini_Index)

Previous Year Inequality =
CALCULATE(
[Avg Gini Index],
PREVIOUSYEAR(Year)
)

Inequality Change % =
DIVIDE(
[Avg Gini Index] - [Previous Year Inequality],
[Previous Year Inequality]
)

""")

# ==================================
# DASHBOARD
# ==================================

elif page == "Dashboard":

    st.title("📊 Interactive Analytics Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,width=1400,height=750)

# ==================================
# INSIGHTS
# ==================================

elif page == "Insights":

    st.title("📊 Key Insights")

    st.markdown("""
    <div class="glass">

    Major findings from the analysis:

    • Several African nations show higher inequality levels  
    • Majority of countries fall into the medium inequality category  
    • Population-weighted inequality highlights economic concentration  
    • Developed regions show relatively stable Gini index trends  

    </div>
    """, unsafe_allow_html=True)

# ==================================
# FAQ
# ==================================

elif page == "FAQ":

    st.title("❓ Frequently Asked Questions")

    with st.expander("What is the Gini Index?"):
        st.write("The Gini Index measures income inequality within a country.")

    with st.expander("What does Palma Ratio represent?"):
        st.write("It compares income share of richest 10% vs poorest 40%.")

    with st.expander("Why is income inequality important?"):
        st.write("High inequality impacts economic growth and social stability.")

    with st.expander("What tools were used in this project?"):
        st.write("Power BI, Python, Streamlit, and data analytics methods.")

# ==================================
# FEEDBACK
# ==================================

elif page == "Feedback":

    st.title("💬 User Feedback")

    with st.form("feedback_form"):

        name = st.text_input("Your Name")
        rating = st.slider("Rate this dashboard",1,5)
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

# ==================================
# ADMIN PANEL
# ==================================

elif page == "Admin Panel":

    st.title("🛠 Admin Panel")

    if os.path.exists("feedback.csv"):

        df_feedback = pd.read_csv("feedback.csv")

        st.dataframe(df_feedback)

        st.metric("Average Rating",round(df_feedback["Rating"].mean(),2))

        st.bar_chart(df_feedback["Rating"].value_counts())

    else:

        st.warning("No feedback data available")

# ==================================
# FOOTER
# ==================================

st.markdown("""
---
<center>

Global Income Distribution Analytics Platform  
End-to-End Data Analytics Project

Built using Power BI • Python • Streamlit

</center>
""", unsafe_allow_html=True)


