import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor

# METRICS
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# -------------------------------
# ULTRA ADVANCED DASHBOARD STYLING
# -------------------------------
st.markdown("""
<style>

/* GLOBAL APP BACKGROUND */
.stApp {
    background: linear-gradient(-45deg,#0f0c29,#302b63,#24243e,#1f2937);
    background-size: 400% 400%;
    animation: gradientBG 18s ease infinite;
    color:white;
    font-family: 'Segoe UI', sans-serif;
}

@keyframes gradientBG {
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}

/* TITLE WITH ANIMATED GLOW */
.title{
    font-size:55px;
    font-weight:900;
    text-align:center;
    background: linear-gradient(270deg,#ff6ec4,#7873f5,#00f2ff,#22d3ee);
    background-size:600% 600%;
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    animation: gradientText 8s ease infinite;
    text-shadow:0 0 25px rgba(255,255,255,0.3);
    margin-bottom:30px;
}

@keyframes gradientText{
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}

/* GLASS PANEL */
.card{
    background:rgba(255,255,255,0.05);
    backdrop-filter:blur(18px);
    border-radius:25px;
    padding:30px;
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 15px 40px rgba(0,0,0,0.4);
    transition:all 0.4s ease;
}

.card:hover{
    transform:translateY(-8px) scale(1.02);
    box-shadow:0 25px 60px rgba(0,0,0,0.6);
}

/* KPI CARDS */
.kpi-card{
    background:linear-gradient(135deg,#1e1b4b,#312e81,#1e293b);
    border-radius:22px;
    padding:30px;
    text-align:center;
    box-shadow:
        0 10px 30px rgba(0,0,0,0.6),
        inset 0 0 20px rgba(255,255,255,0.05);
    transition:all 0.35s ease;
    position:relative;
    overflow:hidden;
}

/* animated border */
.kpi-card::before{
    content:"";
    position:absolute;
    inset:-2px;
    background:linear-gradient(270deg,#6366f1,#06b6d4,#f59e0b,#ec4899);
    background-size:600% 600%;
    animation:borderGlow 6s linear infinite;
    z-index:-1;
    filter:blur(12px);
}

@keyframes borderGlow{
  0%{background-position:0%}
  100%{background-position:400%}
}

.kpi-card:hover{
    transform:scale(1.08) rotateX(6deg) rotateY(6deg);
    box-shadow:
        0 20px 50px rgba(0,0,0,0.8),
        0 0 25px #6366f1;
}

/* KPI NUMBER */
.kpi-number{
    font-size:48px;
    font-weight:900;
    background:linear-gradient(90deg,#a78bfa,#06b6d4,#f59e0b);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

/* KPI LABEL */
.kpi-label{
    font-size:16px;
    letter-spacing:1px;
    color:#e5e7eb;
    margin-top:8px;
    text-transform:uppercase;
}

/* SIDEBAR STYLE */
section[data-testid="stSidebar"]{
  background:linear-gradient(180deg,#020617,#111827,#020617);
  border-right:1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR ITEMS */
section[data-testid="stSidebar"] div[role="radiogroup"] > label{
  transition:all 0.3s ease;
  border-radius:14px;
  padding:10px 14px;
  margin-bottom:5px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover{
  background:linear-gradient(90deg,#6366f1,#a855f7,#06b6d4);
  color:#fff;
  transform:scale(1.06);
  box-shadow:0 8px 20px rgba(99,102,241,0.4);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"]{
  background:linear-gradient(90deg,#f59e0b,#22d3ee);
  color:#fff;
  border:2px solid #fff;
  box-shadow:0 0 18px #f59e0b,0 0 18px #22d3ee;
}

/* STREAMLIT BUTTONS */
.stButton>button{
    background:linear-gradient(90deg,#6366f1,#a855f7);
    color:white;
    border:none;
    border-radius:10px;
    padding:8px 16px;
    font-weight:600;
    transition:all 0.3s ease;
}

.stButton>button:hover{
    transform:scale(1.05);
    box-shadow:0 5px 15px rgba(99,102,241,0.5);
}

/* CHART CONTAINERS */
.css-1r6slb0{
    background:rgba(255,255,255,0.03);
    border-radius:20px;
    padding:15px;
    box-shadow:0 10px 25px rgba(0,0,0,0.5);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# ADVANCED SIDEBAR EFFECTS
# -------------------------------
st.markdown("""
<style>

/* SIDEBAR BACKGROUND */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#020617,#0f172a,#020617);
    border-right: 2px solid rgba(255,255,255,0.1);
    animation: sidebarGlow 8s infinite alternate;
}

/* SIDEBAR GLOW ANIMATION */
@keyframes sidebarGlow{
    0%{box-shadow: 0 0 10px #6366f1}
    50%{box-shadow: 0 0 25px #06b6d4}
    100%{box-shadow: 0 0 10px #a855f7}
}

/* SIDEBAR TITLE */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    background: linear-gradient(90deg,#a78bfa,#06b6d4,#f59e0b);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    font-weight:900;
}

/* NAVIGATION ITEMS */
section[data-testid="stSidebar"] div[role="radiogroup"] > label{
    border-radius:14px;
    padding:10px 14px;
    margin-bottom:6px;
    transition: all 0.3s ease;
    background: rgba(255,255,255,0.03);
}

/* HOVER EFFECT */
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover{
    transform: scale(1.08);
    background: linear-gradient(90deg,#6366f1,#a855f7,#06b6d4);
    color:#fff;
    box-shadow:
        0 0 10px #6366f1,
        0 0 20px #06b6d4,
        0 0 30px #a855f7;
}

/* ACTIVE SELECTED ITEM */
section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"]{
    background: linear-gradient(90deg,#f59e0b,#22d3ee);
    color:#fff;
    font-weight:700;
    border:2px solid #fff;
    box-shadow:
        0 0 12px #f59e0b,
        0 0 25px #22d3ee;
}

/* SIDEBAR SECTION DIVIDER */
.sidebar-section{
    font-size:14px;
    font-weight:700;
    color:#94a3b8;
    margin-top:20px;
    margin-bottom:5px;
    text-transform:uppercase;
    letter-spacing:1px;
    border-left:3px solid #6366f1;
    padding-left:8px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()
numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# -------------------------------
# ADVANCED LOGIN SYSTEM
# -------------------------------

import streamlit as st
import hashlib
import time

# -------------------------------
# USER DATABASE
# -------------------------------

users = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Admin"
    },
    "analyst": {
        "password": hashlib.sha256("data123".encode()).hexdigest(),
        "role": "Analyst"
    },
    "viewer": {
        "password": hashlib.sha256("view123".encode()).hexdigest(),
        "role": "Viewer"
    }
}

# -------------------------------
# SESSION STATE INITIALIZATION
# -------------------------------

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.login_attempts = 0
    st.session_state.last_activity = time.time()

# -------------------------------
# SESSION TIMEOUT (10 MINUTES)
# -------------------------------

TIMEOUT = 600

if st.session_state.login:
    if time.time() - st.session_state.last_activity > TIMEOUT:
        st.session_state.login = False
        st.warning("Session expired. Please login again.")
        st.rerun()

# -------------------------------
# LOGIN SCREEN
# -------------------------------

if not st.session_state.login:

    st.markdown(
        "<div class='title'>🌍 Global Income Intelligence Platform</div>",
        unsafe_allow_html=True
    )

    st.markdown("### 🔐 Secure Login")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        login_btn = st.button("🚀 Login")

    with col2:
        st.button("🔑 Forgot Password")

    if login_btn:

        hashed_pw = hashlib.sha256(password.encode()).hexdigest()

        if username in users and users[username]["password"] == hashed_pw:

            st.session_state.login = True
            st.session_state.user = username
            st.session_state.role = users[username]["role"]
            st.session_state.last_activity = time.time()
            st.success("Login successful")
            time.sleep(1)
            st.rerun()

        else:

            st.session_state.login_attempts += 1
            st.error("Invalid username or password")

            if st.session_state.login_attempts >= 3:
                st.warning("Too many attempts. Please wait 10 seconds.")
                time.sleep(10)

    st.stop()

# -------------------------------
# USER HEADER
# -------------------------------

st.sidebar.markdown("### 👤 User Info")
st.sidebar.write("User:", st.session_state.user)
st.sidebar.write("Role:", st.session_state.role)

# -------------------------------
# LOGOUT BUTTON
# -------------------------------

if st.sidebar.button("🚪 Logout"):
    st.session_state.login = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# -------------------------------
# UPDATE ACTIVITY TIMER
# -------------------------------

st.session_state.last_activity = time.time()


# -------------------------------
# ULTRA ADVANCED SIDEBAR NAVIGATION
# -------------------------------

import streamlit as st

# -------------------------------
# SIDEBAR HEADER
# -------------------------------

st.sidebar.markdown("""
<div style="
text-align:center;
padding:14px;
border-radius:14px;
background:linear-gradient(135deg,#1e293b,#0f172a);
border:1px solid rgba(255,255,255,0.1);
box-shadow:0 6px 25px rgba(0,0,0,0.6);
">

<h2 style="
color:white;
font-weight:800;
letter-spacing:1px;
text-shadow:0 0 10px rgba(0,0,0,0.8);
margin-bottom:4px;
">
🚀 Global Data Analytics Platform
</h2>

<p style="
font-size:14px;
color:#cbd5f5;
margin-top:0;
">
Analytics Platform
</p>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# -------------------------------
# USER PROFILE CARD
# -------------------------------

st.sidebar.markdown("""
<div style="
padding:12px;
border-radius:12px;
background:rgba(255,255,255,0.05);
backdrop-filter:blur(10px);
text-align:center;
box-shadow:0 5px 20px rgba(0,0,0,0.4);
">
<h4>👤 Welcome Analyst</h4>
<p style="font-size:12px;color:#ccc;">Enterprise BI Workspace</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# -------------------------------
# MODULE SELECTOR
# -------------------------------

nav_section = st.sidebar.selectbox(
"📂 Select Analytics Module",
[
"🏠 Overview",
"📊 Dashboards",
"🧾 Data Exploration",
"🤖 AI Analytics",
"🧠 Machine Learning",
"📈 Forecasting",
"📄 Reports",
"❓ Help Center"
]
)

# -------------------------------
# OVERVIEW
# -------------------------------

if nav_section == "🏠 Overview":

    menu = st.sidebar.radio(
    "Navigation",
    [
    "🏠 Introduction",
    "🏠 Executive Dashboard"
    ])

# -------------------------------
# DASHBOARDS
# -------------------------------

elif nav_section == "📊 Dashboards":

    menu = st.sidebar.radio(
    "Dashboard Pages",
    [
    "📘 Dashboard Guide",
    "📊 Power BI Dashboard"
    ])

# -------------------------------
# DATA EXPLORATION
# -------------------------------

elif nav_section == "🧾 Data Exploration":

    menu = st.sidebar.radio(
    "Explore Data",
    [
    "🧾 Dataset Explorer",
    "📈 Chart Explorer",
    "🌐 Country Comparison",
    "🌍 Country Analysis",
    "🗺 Global Map Visualization"
    ])

# -------------------------------
# AI ANALYTICS
# -------------------------------

elif nav_section == "🤖 AI Analytics":

    menu = st.sidebar.radio(
    "AI Tools",
    [
    "🤖 AI Insights Generator"
    ])

# -------------------------------
# MACHINE LEARNING
# -------------------------------

elif nav_section == "🧠 Machine Learning":

    menu = st.sidebar.radio(
    "ML Models",
    [
    "🧠 Machine Learning Prediction",
    "⚡ Auto ML Prediction"
    ])

# -------------------------------
# FORECASTING
# -------------------------------

elif nav_section == "📈 Forecasting":

    menu = st.sidebar.radio(
    "Forecasting Tools",
    [
    "⏳ Time Series Forecasting"
    ])

# -------------------------------
# REPORTS
# -------------------------------

elif nav_section == "📄 Reports":

    menu = st.sidebar.radio(
    "Reports",
    [
    "📄 Generate PDF Report"
    ])

# -------------------------------
# HELP
# -------------------------------

elif nav_section == "❓ Help Center":

    menu = st.sidebar.radio(
    "Help Center",
    [
    "❓ FAQ",
    "ℹ About"
    ])

st.sidebar.markdown("---")

# -------------------------------
# QUICK STATS PANEL
# -------------------------------

st.sidebar.markdown("### 📊 Platform Stats")

col1, col2 = st.sidebar.columns(2)

with col1:
    st.metric("Countries", 200)

with col2:
    st.metric("Models", 5)

st.sidebar.metric("Dataset Records", "1.2M")

st.sidebar.markdown("---")

# -------------------------------
# SYSTEM STATUS
# -------------------------------

st.sidebar.markdown("### ⚡ System Status")

st.sidebar.success("AI Engine Online")
st.sidebar.info("Data Updated Today")

st.sidebar.markdown("---")

# -------------------------------
# THEME SWITCHER
# -------------------------------

theme = st.sidebar.toggle("🌙 Dark Mode", value=True)

if theme:
    st.sidebar.write("Dark theme enabled")
else:
    st.sidebar.write("Light theme enabled")



# -------------------------------
# INTRODUCTION
# -------------------------------

if menu == "🏠 Introduction":

    st.markdown("<div class='title'>Introduction</div>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.markdown(f"<div class='kpi-card'><div class='kpi-number'>62.49</div><div class='kpi-label'>Inequality Range</div></div>",unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi-card'><div class='kpi-number'>37.52</div><div class='kpi-label'>Avg Gini Index</div></div>",unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi-card'><div class='kpi-number'>22.55</div><div class='kpi-label'>Avg Inequality Index</div></div>",unsafe_allow_html=True)
    col4.markdown(f"<div class='kpi-card'><div class='kpi-number'>200</div><div class='kpi-label'>Total Countries</div></div>",unsafe_allow_html=True)
    col5.markdown(f"<div class='kpi-card'><div class='kpi-number'>7.85bn</div><div class='kpi-label'>Total Population</div></div>",unsafe_allow_html=True)

    st.markdown("""

# Project Title  
### Interactive Analytics Dashboard for Global Income Distribution

---

# 1. Project Overview

The **Interactive Analytics Dashboard for Global Income Distribution** is a data analytics platform designed to explore global income inequality using modern visualization tools and machine learning techniques.  

Income inequality is one of the most important global economic issues affecting societies worldwide. Governments, researchers, and organizations often analyze inequality indicators such as the **Gini Index** and **Income Distribution Metrics** to understand how wealth is distributed across populations.

However, analyzing such data using spreadsheets or static reports can be extremely difficult. Large datasets often hide valuable insights that are not easily visible without interactive tools.

This project solves that problem by building a **fully interactive analytics dashboard** that allows users to explore global income distribution in a visually engaging way.

The platform integrates **data analysis, visualization, and machine learning** into one unified interface.

---

# 2. Purpose of the Project

The purpose of this project is to create a powerful analytical tool that enables users to explore patterns of income inequality across different countries and time periods.

The dashboard allows users to:

• Understand global inequality trends  
• Compare countries based on income distribution metrics  
• Analyze changes in inequality over time  
• Visualize data using advanced charts  
• Predict future inequality values using machine learning  

By transforming raw economic data into meaningful visualizations, the platform helps users gain deeper insights into global economic patterns.

---

# 3. Problem Statement

Understanding global income inequality can be challenging due to several factors:

• Large and complex datasets  
• Lack of interactive analytical tools  
• Difficulty identifying trends from static reports  
• Limited accessibility for non-technical users  

Traditional analysis methods often require significant technical expertise. This project aims to simplify the process by providing an **interactive dashboard that anyone can use**.

---

# 4. Dataset Description

The dataset used in this project contains information about global income distribution and inequality indicators across multiple countries and years.

Key variables included in the dataset:

• Country name  
• Year of observation  
• Population statistics  
• Gini Index values  
• Inequality Index values  
• Income distribution indicators  

These variables allow users to analyze both **geographical patterns** and **historical trends** in income inequality.

---

# 5. Data Preparation Process

Before building the dashboard, several data preprocessing steps were performed to ensure the dataset was clean and reliable.

### Data Cleaning
Raw datasets often contain inconsistencies such as missing values, incorrect formatting, or duplicate records. These issues were addressed through data cleaning techniques.

### Handling Missing Values
Missing data points were handled using methods such as:

• removing incomplete records  
• replacing values with averages  
• interpolation for time-series variables  

### Data Transformation
Certain variables were transformed into formats suitable for visualization and machine learning models.

---

# 6. Tools and Technologies Used

This project was built using modern data science and analytics technologies.

### Dashboard Development
The dashboard interface was built using **Streamlit**, a Python framework that enables the creation of interactive web applications for data analysis.

### Data Processing
Data manipulation and analysis were performed using the **Pandas** library.

### Data Visualization
Interactive charts were created using **Plotly**, which allows dynamic exploration of datasets.

### Machine Learning
Predictive analytics were implemented using **Scikit-learn** models including:

• Linear Regression  
• Random Forest Regression  

### Report Generation
PDF reports are generated using **ReportLab**.

---

# 7. Dashboard Features

The dashboard includes several modules designed for different types of analysis.

### Executive Dashboard
Provides an overview of key dataset statistics such as total countries, population, and inequality metrics.

### Data Explorer
Allows users to inspect the dataset and understand variable distributions.

### Interactive Charts
Users can visualize relationships between variables using scatter plots, histograms, and bar charts.

### Country Analysis
Provides country-level insights into income distribution metrics.

### Machine Learning Prediction
Allows users to predict income distribution metrics for specific years using regression models.

### Forecasting Engine
Generates forecasts for future inequality values based on historical data patterns.

---

# 8. User Interface Design

The dashboard uses a modern **glassmorphism design style** that improves visual appeal and usability.

Key UI elements include:

• gradient backgrounds  
• transparent glass cards  
• animated hover effects  
• responsive layout  

These design choices make the dashboard visually engaging while maintaining clarity.

---

# 9. Analytical Insights

Using this dashboard, users can discover valuable insights such as:

• which countries have the highest inequality levels  
• how inequality changes over time  
• correlations between economic indicators  
• patterns in global income distribution  

---

# 10. Real-World Applications

This dashboard can be used in multiple domains including:

• economic research  
• public policy analysis  
• academic education  
• international development studies  

Organizations analyzing global inequality can use such platforms to support evidence-based decision making.

---

# 11. Project Outcome

The final outcome of this project is a **fully functional interactive dashboard** capable of transforming complex global datasets into clear visual insights.

The project demonstrates the power of combining **data science, visualization, and machine learning** to analyze real-world socioeconomic challenges.

---

# 12. Future Improvements

Future versions of the dashboard could include:

• real-time economic data integration  
• advanced forecasting models  
• anomaly detection algorithms  
• AI-driven insight generation  
• deployment on cloud platforms  

These enhancements could transform the dashboard into a large-scale analytics platform.

---

# 13. Conclusion

The **Interactive Analytics Dashboard for Global Income Distribution** highlights how modern data analytics tools can help us better understand global economic inequality.

By combining powerful visualization techniques with predictive analytics, this platform provides an intuitive and accessible way to explore complex economic datasets.

The project demonstrates how data science can be used to create impactful tools for understanding global challenges.

""", unsafe_allow_html=True)

# -------------------------------
# EXECUTIVE DASHBOARD
# -------------------------------
elif menu=="🏠 Executive Dashboard":

    st.markdown("<div class='title'>Executive Analytics Dashboard</div>",unsafe_allow_html=True)

    rows,cols=df.shape
    missing=df.isnull().sum().sum()
    duplicates=df.duplicated().sum()

    quality_score = int((1-(missing/(rows*cols) + duplicates/rows))*100)

    # -------------------------
    # KPI CARDS
    # -------------------------

    col1,col2,col3,col4,col5=st.columns(5)

    col1.markdown(f"<div class='kpi-card'><div class='kpi-number'>{rows}</div><div class='kpi-label'>Total Rows</div></div>",unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi-card'><div class='kpi-number'>{cols}</div><div class='kpi-label'>Total Columns</div></div>",unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi-card'><div class='kpi-number'>{len(numeric_cols)}</div><div class='kpi-label'>Numeric Features</div></div>",unsafe_allow_html=True)
    col4.markdown(f"<div class='kpi-card'><div class='kpi-number'>{len(categorical_cols)}</div><div class='kpi-label'>Categorical Features</div></div>",unsafe_allow_html=True)
    col5.markdown(f"<div class='kpi-card'><div class='kpi-number'>{quality_score}%</div><div class='kpi-label'>Data Quality</div></div>",unsafe_allow_html=True)

    st.divider()

    # -------------------------
    # DATASET PREVIEW
    # -------------------------

    st.subheader("📊 Dataset Preview")

    st.dataframe(df.head(10))

    # -------------------------
    # DATASET INSIGHTS
    # -------------------------

    st.subheader("🧠 Dataset Health")

    col1,col2=st.columns(2)

    col1.markdown(
        f"<div class='card'><h4>Missing Values</h4><p>{missing} missing values detected.</p></div>",
        unsafe_allow_html=True
    )

    col2.markdown(
        f"<div class='card'><h4>Duplicate Rows</h4><p>{duplicates} duplicate rows found.</p></div>",
        unsafe_allow_html=True
    )

    # -------------------------
    # METRIC ANALYTICS
    # -------------------------

    if len(numeric_cols)>0:

        st.subheader("📈 Metric Analytics")

        metric = st.selectbox("Select Metric", numeric_cols)

        col1,col2=st.columns(2)

        with col1:

            fig = px.histogram(
                df,
                x=metric,
                title=f"{metric} Distribution"
            )

            st.plotly_chart(fig,use_container_width=True)

        with col2:

            fig2 = px.box(
                df,
                y=metric,
                title=f"{metric} Outlier Analysis"
            )

            st.plotly_chart(fig2,use_container_width=True)

    # -------------------------
    # CORRELATION HEATMAP
    # -------------------------

    if len(numeric_cols)>1:

        st.subheader("🔥 Feature Correlation Matrix")

        corr=df[numeric_cols].corr()

        fig3=px.imshow(
            corr,
            text_auto=True,
            aspect="auto"
        )

        st.plotly_chart(fig3,use_container_width=True)

    # -------------------------
    # CATEGORY ANALYSIS
    # -------------------------

    if len(categorical_cols)>0:

        st.subheader("📊 Category Analysis")

        cat = st.selectbox("Select Category", categorical_cols)

        counts = df[cat].value_counts().reset_index()

        counts.columns=[cat,"Count"]

        fig4=px.bar(
            counts,
            x=cat,
            y="Count",
            color="Count",
            title=f"{cat} Distribution"
        )

        st.plotly_chart(fig4,use_container_width=True)

    # -------------------------
    # FEATURE RANKING
    # -------------------------

    if len(numeric_cols)>1:

        st.subheader("🏆 Feature Ranking")

        mean_values = df[numeric_cols].mean().sort_values(ascending=False)

        rank_df = mean_values.reset_index()

        rank_df.columns=["Feature","Mean"]

        fig5=px.bar(
            rank_df,
            x="Feature",
            y="Mean",
            title="Feature Importance (Mean Value Ranking)"
        )

        st.plotly_chart(fig5,use_container_width=True)

    # -------------------------
    # EXECUTIVE AI INSIGHTS
    # -------------------------

    st.subheader("🤖 Executive Insights")

    insights=[]

    if missing>0:
        insights.append("Dataset contains missing values that may affect reporting accuracy.")

    if duplicates>0:
        insights.append("Duplicate records detected — data cleaning recommended.")

    if quality_score>90:
        insights.append("Dataset quality is excellent and ready for analytics.")

    if len(numeric_cols)>10:
        insights.append("High number of numeric features detected — dimensionality reduction may help modeling.")

    if len(insights)==0:
        insights.append("Dataset appears healthy with balanced structure.")

    for i in insights:
        st.info(i)

    # -------------------------
    # EXECUTIVE RECOMMENDATIONS
    # -------------------------

    st.subheader("📑 Executive Recommendations")

    rec=[]

    if missing>0:
        rec.append("Implement data imputation strategies.")

    if duplicates>0:
        rec.append("Remove duplicate rows to improve analysis reliability.")

    if len(numeric_cols)>5:
        rec.append("Apply feature selection to improve ML performance.")

    if len(rec)==0:
        rec.append("Dataset is analytics-ready.")

    for r in rec:
        st.success(r)

# -------------------------------
# DASHBOARD GUIDE
# -------------------------------
elif menu=="📘 Dashboard Guide":

    st.markdown("<div class='title'>Platform User Guide</div>",unsafe_allow_html=True)

    st.markdown("""

# 🌍 Global Income Intelligence Platform – Complete User Guide

Welcome to the **Global Income Intelligence Platform**.  
This dashboard is designed to help users explore global income distribution, analyze inequality trends, and generate insights using interactive visualizations and machine learning models.

This guide explains each module of the platform and how to use them effectively.

---

# 1️⃣ Executive Dashboard

The **Executive Dashboard** provides a high-level overview of the dataset.

This section is designed for quick insights and decision-making. It summarizes the most important statistics from the dataset and presents them through key performance indicators (KPIs).

Key elements available in this dashboard include:

• Total number of records in the dataset  
• Total number of countries included in the analysis  
• Average Gini Index across all countries  
• Average Inequality Index values  
• Population statistics  

These metrics help users quickly understand the scale and distribution of the dataset before diving deeper into detailed analysis.

The Executive Dashboard acts as the **central overview panel** for the entire platform.

---

# 2️⃣ Power BI Dashboard

This section embeds a professional **business intelligence dashboard**.

It integrates an external enterprise visualization environment into the platform.

Features of this module include:

• Advanced interactive charts  
• Drill-down analytics  
• Pre-built business intelligence reports  
• enterprise-level visual analytics  

Users can interact with the embedded dashboard directly within the application.

This module demonstrates how modern analytics platforms integrate with enterprise BI systems to deliver powerful data insights.

---

# 3️⃣ Dataset Explorer

The **Dataset Explorer** allows users to inspect the raw dataset used in the platform.

This module provides detailed access to the dataset structure and statistics.

Users can:

• View all dataset rows and columns  
• Explore column types  
• Analyze statistical summaries  
• Identify missing values  
• Understand variable distributions  

This section is especially useful for:

• data scientists  
• analysts  
• researchers  

It allows them to understand the dataset before performing advanced analysis.

---

# 4️⃣ Chart Explorer

The **Chart Explorer** is a dynamic visualization environment that allows users to generate interactive charts.

Users can create various visualizations such as:

• Histograms  
• Scatter plots  
• Line charts  
• Box plots  
• Heatmaps  

These visualizations help users identify relationships between variables, detect patterns in income distribution, and uncover hidden insights in the data.

The interactive nature of the charts allows users to zoom, filter, and hover over data points for additional information.

---

# 5️⃣ AI Insights Generator

The **AI Insights Generator** automatically analyzes the dataset and generates statistical insights.

Instead of manually calculating statistics, the platform automatically computes:

• mean values  
• standard deviation  
• maximum values  
• minimum values  
• distribution ranges  

These insights help users quickly understand the characteristics of each variable without performing manual calculations.

This module acts as an **automated analytics assistant**.

---

# 6️⃣ Country Analysis

The **Country Analysis module** allows users to explore inequality metrics for specific countries.

Users can select a country and examine its economic indicators.

This module helps answer questions such as:

• Which countries have the highest income inequality?  
• How does inequality vary across regions?  
• What are the trends in a specific country?  

Visual charts provide a clear representation of country-level inequality metrics.

---

# 7️⃣ Global Map Visualization

This section displays a **global geographic visualization** of income distribution.

Using a world map, users can analyze inequality indicators across different countries.

Features include:

• interactive world map  
• color-coded inequality levels  
• geographic comparison of income distribution  
• quick identification of high and low inequality regions  

This visualization provides a spatial understanding of economic inequality.

---

# 8️⃣ Machine Learning Prediction

The **Machine Learning Prediction module** uses predictive analytics to estimate future values.

The model uses historical data and applies **Linear Regression** to generate predictions.

Users can input a year or variable and obtain predicted values for inequality indicators.

This module demonstrates how machine learning can be applied to economic datasets.

---

# 9️⃣ Auto ML Prediction

The **Auto ML Prediction system** compares multiple machine learning models to determine the best-performing model.

Instead of manually selecting an algorithm, the system evaluates models such as:

• Linear Regression  
• Random Forest  
• Decision Tree  

The model with the highest performance is selected automatically.

This feature improves prediction accuracy and simplifies the machine learning workflow.

---

# 🔟 Time Series Forecasting

The **Time Series Forecasting module** analyzes historical trends in inequality metrics.

By studying patterns over time, the system can forecast future trends.

This helps answer questions such as:

• Will inequality increase in the future?  
• Are current trends improving or worsening?  
• What are the long-term projections for income distribution?

Forecasting charts visually represent predicted future trends.

---

# 1️⃣1️⃣ Generate PDF Report

The **Report Generation module** allows users to export analytical results.

Users can download a **PDF summary report** containing:

• dataset statistics  
• analytical insights  
• summary metrics  

This feature is useful for sharing insights with stakeholders, researchers, or policymakers.

---

# 1️⃣2️⃣ FAQ & About Section

The **FAQ and About module** provides helpful information about the platform.

It includes details such as:

• project purpose  
• technologies used  
• data sources  
• guidance for new users  

This section ensures users understand how the platform works and how to use its features effectively.

---

# 🧠 Final Notes

The **Global Income Intelligence Platform** combines modern data analytics tools with machine learning to create a powerful analytical environment.

Through interactive dashboards, predictive analytics, and automated insights, users can better understand the complex issue of global income inequality.

This platform demonstrates how data science and visualization technologies can transform raw data into meaningful insights.

""",unsafe_allow_html=True)

# -------------------------------
# ENTERPRISE BI PORTAL
# -------------------------------
elif menu=="📊 Power BI Dashboard":

    import numpy as np
    from sklearn.ensemble import IsolationForest
    from datetime import datetime
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    st.title("📊 Enterprise Business Intelligence Portal")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    # ---------------------------------
    # THEME TOGGLE
    # ---------------------------------

    theme = st.toggle("🌙 Dark Mode")

    if theme:
        st.markdown(
        """
        <style>
        .stApp {background-color:#0E1117;color:white;}
        </style>
        """,
        unsafe_allow_html=True
        )

    # ---------------------------------
    # DASHBOARD TABS
    # ---------------------------------

    tab1,tab2,tab3,tab4 = st.tabs([
        "📊 Dashboard",
        "🧠 AI Insights",
        "🚨 KPI Alerts",
        "📑 Reports"
    ])

    # =================================
    # TAB 1 — DASHBOARD
    # =================================

    with tab1:

        st.subheader("📈 Business KPI Overview")

        rows,cols=df.shape
        missing=df.isnull().sum().sum()
        duplicates=df.duplicated().sum()

        c1,c2,c3,c4=st.columns(4)

        c1.metric("Rows",rows)
        c2.metric("Columns",cols)
        c3.metric("Missing",missing)
        c4.metric("Duplicates",duplicates)

        st.divider()

        # -----------------------------
        # HYBRID STREAMLIT ANALYTICS
        # -----------------------------

        st.subheader("📊 Hybrid Analytics")

        if len(numeric_cols)>0:

            metric=st.selectbox("Select Metric",numeric_cols)

            fig=px.line(
                df,
                y=metric,
                title=f"{metric} Trend"
            )

            st.plotly_chart(fig,use_container_width=True)

            fig2=px.histogram(
                df,
                x=metric,
                title=f"{metric} Distribution"
            )

            st.plotly_chart(fig2,use_container_width=True)

        # -----------------------------
        # POWER BI EMBED
        # -----------------------------

        st.subheader("📊 Power BI Interactive Dashboard")

        height=st.slider("Dashboard Height",600,1200,800)

        st.components.v1.iframe(
            powerbi_url,
            height=height,
            scrolling=True
        )

        st.link_button("🔗 Open Full Power BI Dashboard",powerbi_url)

    # =================================
    # TAB 2 — AI INSIGHTS
    # =================================

    with tab2:

        st.subheader("🧠 AI Business Insights Generator")

        insights=[]

        if missing>0:
            insights.append("Dataset contains missing values that may impact analytics.")

        if duplicates>0:
            insights.append("Duplicate records detected. Data cleaning recommended.")

        if len(numeric_cols)>0:

            skew=df[numeric_cols].skew()

            high_skew=skew[abs(skew)>1]

            if len(high_skew)>0:
                insights.append("Highly skewed features detected.")

        if len(insights)==0:
            insights.append("Dataset appears healthy with balanced features.")

        for i in insights:
            st.info(i)

        # -----------------------------
        # CHART EXPLANATION
        # -----------------------------

        st.subheader("📊 AI Chart Explanation")

        if len(numeric_cols)>0:

            col=st.selectbox("Explain Column",numeric_cols)

            mean=df[col].mean()
            median=df[col].median()
            std=df[col].std()

            st.write(f"""
            **AI Summary**

            • Average value of {col} is **{round(mean,2)}**

            • Median value is **{round(median,2)}**

            • Standard deviation is **{round(std,2)}**

            This suggests the distribution may contain variability depending on the deviation level.
            """)

    # =================================
    # TAB 3 — KPI ALERTS
    # =================================

    with tab3:

        st.subheader("🚨 Real-Time KPI Anomaly Detection")

        if len(numeric_cols)>0:

            column=st.selectbox("Select KPI Metric",numeric_cols)

            data=df[[column]].dropna()

            model=IsolationForest(contamination=0.05)

            preds=model.fit_predict(data)

            data["Anomaly"]=preds

            anomalies=data[data["Anomaly"]==-1]

            fig=px.scatter(
                data,
                y=column,
                color=data["Anomaly"].astype(str),
                title="KPI Anomaly Detection"
            )

            st.plotly_chart(fig,use_container_width=True)

            st.write("Detected anomalies:",len(anomalies))

            if len(anomalies)>0:
                st.warning("⚠ Potential KPI anomalies detected!")

    # =================================
    # TAB 4 — REPORT GENERATION
    # =================================

    with tab4:

        st.subheader("📑 Automated Business Report")

        if st.button("Generate PDF Report"):

            styles=getSampleStyleSheet()

            report_text=[
                Paragraph("Business Intelligence Report",styles["Title"]),
                Spacer(1,20),
                Paragraph(f"Generated: {datetime.now()}",styles["Normal"]),
                Spacer(1,20),
                Paragraph(f"Rows: {rows}",styles["Normal"]),
                Paragraph(f"Columns: {cols}",styles["Normal"]),
                Paragraph(f"Missing Values: {missing}",styles["Normal"]),
                Paragraph(f"Duplicate Rows: {duplicates}",styles["Normal"]),
            ]

            pdf_file="bi_report.pdf"

            doc=SimpleDocTemplate(pdf_file)

            doc.build(report_text)

            with open(pdf_file,"rb") as f:

                st.download_button(
                    "Download Report",
                    f,
                    file_name="BI_Report.pdf"
                )

# -------------------------------
# NEXT LEVEL DATASET EXPLORER
# -------------------------------
elif menu=="🧾 Dataset Explorer":

    st.title("🧾 AI Dataset Explorer")

    # -----------------------------
    # DATASET OVERVIEW
    # -----------------------------

    st.subheader("📊 Dataset Overview")

    rows,cols = df.shape
    missing_total = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    col1,col2,col3,col4 = st.columns(4)

    col1.metric("Rows", rows)
    col2.metric("Columns", cols)
    col3.metric("Missing Values", missing_total)
    col4.metric("Duplicates", duplicates)

    st.dataframe(df.head(50))

    # -----------------------------
    # DATA QUALITY SCORE
    # -----------------------------

    st.subheader("⚡ Data Quality Score")

    missing_ratio = missing_total/(rows*cols)
    duplicate_ratio = duplicates/rows

    quality_score = int((1-(missing_ratio+duplicate_ratio))*100)

    st.progress(quality_score/100)

    st.success(f"Dataset Quality Score: {quality_score}/100")

    # -----------------------------
    # AUTOMATIC EDA REPORT
    # -----------------------------

    st.subheader("📊 Automatic EDA Summary")

    eda = pd.DataFrame({
        "Column":df.columns,
        "Type":df.dtypes,
        "Missing":df.isnull().sum(),
        "Unique":df.nunique()
    })

    st.dataframe(eda)

    # -----------------------------
    # SKEWNESS & KURTOSIS
    # -----------------------------

    st.subheader("📉 Skewness & Kurtosis")

    skew_df = pd.DataFrame({
        "Skewness":df[numeric_cols].skew(),
        "Kurtosis":df[numeric_cols].kurt()
    })

    st.dataframe(skew_df)

    fig1 = px.bar(
        skew_df,
        barmode="group",
        title="Skewness & Kurtosis"
    )

    st.plotly_chart(fig1,use_container_width=True)

    # -----------------------------
    # OUTLIER DETECTION
    # -----------------------------

    st.subheader("🧠 Outlier Detection")

    outlier_counts = {}

    for col in numeric_cols:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3-Q1

        lower = Q1-1.5*IQR
        upper = Q3+1.5*IQR

        outliers = df[(df[col]<lower)|(df[col]>upper)]

        outlier_counts[col] = len(outliers)

    outlier_df = pd.DataFrame(
        list(outlier_counts.items()),
        columns=["Column","Outliers"]
    )

    st.dataframe(outlier_df)

    fig2 = px.bar(
        outlier_df,
        x="Column",
        y="Outliers",
        color="Outliers",
        title="Outlier Count"
    )

    st.plotly_chart(fig2,use_container_width=True)

    # -----------------------------
    # CORRELATION MATRIX
    # -----------------------------

    st.subheader("🔥 Feature Correlation")

    corr = df[numeric_cols].corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto"
    )

    st.plotly_chart(fig3,use_container_width=True)

    # -----------------------------
    # FEATURE IMPORTANCE
    # -----------------------------

    st.subheader("🔍 Feature Importance Ranking")

    if len(numeric_cols) > 1:

        target = st.selectbox("Select Target", numeric_cols)

        features = [c for c in numeric_cols if c!=target]

        X = df[features].fillna(0)
        y = df[target].fillna(0)

        model = RandomForestRegressor()

        model.fit(X,y)

        importance = model.feature_importances_

        imp_df = pd.DataFrame({
            "Feature":features,
            "Importance":importance
        }).sort_values("Importance",ascending=False)

        fig4 = px.bar(
            imp_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance"
        )

        st.plotly_chart(fig4,use_container_width=True)

    # -----------------------------
    # AI DATA INSIGHTS
    # -----------------------------

    st.subheader("🤖 AI Data Insights")

    insights = []

    if missing_total > 0:
        insights.append("Dataset contains missing values that may affect model performance.")

    if duplicates > 0:
        insights.append("Duplicate rows detected. Consider removing duplicates.")

    high_skew = skew_df[abs(skew_df["Skewness"])>1]

    if len(high_skew)>0:
        insights.append("Highly skewed features detected. Consider log transformation.")

    if outlier_df["Outliers"].sum()>0:
        insights.append("Outliers detected in multiple columns.")

    if len(insights)==0:
        insights.append("Dataset appears clean and well balanced.")

    for i in insights:
        st.info(i)

    # -----------------------------
    # DATA CLEANING SUGGESTIONS
    # -----------------------------

    st.subheader("📑 Auto Data Cleaning Suggestions")

    suggestions = []

    if missing_total>0:
        suggestions.append("Fill missing values using mean/median or drop rows.")

    if duplicates>0:
        suggestions.append("Remove duplicate rows.")

    if outlier_df["Outliers"].sum()>0:
        suggestions.append("Handle outliers using IQR filtering or winsorization.")

    suggestions.append("Normalize or scale numeric features before ML modeling.")

    for s in suggestions:
        st.write("•",s)

    # -----------------------------
    # DOWNLOAD DATASET
    # -----------------------------

    st.subheader("📥 Download Dataset")

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "dataset.csv"
    )

# -------------------------------
# ADVANCED CHART EXPLORER
# -------------------------------
elif menu=="📈 Chart Explorer":

    st.title("📈 Advanced Chart Explorer")

    chart_type = st.selectbox(
        "Select Chart Type",
        [
            "Histogram",
            "Box Plot",
            "Scatter Plot",
            "Line Chart",
            "Bar Chart",
            "Area Chart",
            "Violin Plot",
            "Bubble Chart",
            "3D Scatter",
            "Pie Chart",
            "Sunburst",
            "Treemap",
            "Density Contour",
            "Correlation Heatmap"
        ]
    )

    # -----------------------------
    # STYLE OPTIONS
    # -----------------------------

    st.sidebar.header("🎨 Chart Customization")

    color_palette = st.sidebar.selectbox(
        "Color Theme",
        ["viridis","plasma","inferno","magma","cividis","blues","reds","greens"]
    )

    template_style = st.sidebar.selectbox(
        "Plot Style",
        ["plotly","plotly_dark","ggplot2","seaborn"]
    )

    marker_size = st.sidebar.slider("Marker Size",5,30,10)

    # -----------------------------
    # HISTOGRAM
    # -----------------------------

    if chart_type == "Histogram":

        col = st.selectbox("Select Column", numeric_cols)

        bins = st.slider("Bins",10,100,30)

        fig = px.histogram(
            df,
            x=col,
            nbins=bins,
            color_discrete_sequence=[px.colors.sequential.Viridis[4]],
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # SCATTER
    # -----------------------------

    elif chart_type == "Scatter Plot":

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)
        color = st.selectbox("Color By", df.columns)

        fig = px.scatter(
            df,
            x=x,
            y=y,
            color=color,
            size_max=marker_size,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # LINE
    # -----------------------------

    elif chart_type == "Line Chart":

        x = st.selectbox("X Axis", df.columns)
        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.line(
            df,
            x=x,
            y=y,
            markers=True,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # BAR
    # -----------------------------

    elif chart_type == "Bar Chart":

        x = st.selectbox("Category", df.columns)
        y = st.selectbox("Value", numeric_cols)

        fig = px.bar(
            df,
            x=x,
            y=y,
            color=x,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # AREA
    # -----------------------------

    elif chart_type == "Area Chart":

        x = st.selectbox("X Axis", df.columns)
        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.area(
            df,
            x=x,
            y=y,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # BOX
    # -----------------------------

    elif chart_type == "Box Plot":

        x = st.selectbox("Category", df.columns)
        y = st.selectbox("Value", numeric_cols)

        fig = px.box(
            df,
            x=x,
            y=y,
            color=x,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # VIOLIN
    # -----------------------------

    elif chart_type == "Violin Plot":

        x = st.selectbox("Category", df.columns)
        y = st.selectbox("Value", numeric_cols)

        fig = px.violin(
            df,
            x=x,
            y=y,
            color=x,
            box=True,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # BUBBLE
    # -----------------------------

    elif chart_type == "Bubble Chart":

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)
        size = st.selectbox("Bubble Size", numeric_cols)

        fig = px.scatter(
            df,
            x=x,
            y=y,
            size=size,
            color=size,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # 3D SCATTER
    # -----------------------------

    elif chart_type == "3D Scatter":

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)
        z = st.selectbox("Z Axis", numeric_cols)

        fig = px.scatter_3d(
            df,
            x=x,
            y=y,
            z=z,
            color=z,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # PIE
    # -----------------------------

    elif chart_type == "Pie Chart":

        col = st.selectbox("Category", categorical_cols)

        fig = px.pie(
            df,
            names=col,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # TREEMAP
    # -----------------------------

    elif chart_type == "Treemap":

        cat = st.selectbox("Category", categorical_cols)
        val = st.selectbox("Value", numeric_cols)

        fig = px.treemap(
            df,
            path=[cat],
            values=val,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # SUNBURST
    # -----------------------------

    elif chart_type == "Sunburst":

        cat = st.selectbox("Category", categorical_cols)
        val = st.selectbox("Value", numeric_cols)

        fig = px.sunburst(
            df,
            path=[cat],
            values=val,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # DENSITY
    # -----------------------------

    elif chart_type == "Density Contour":

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.density_contour(
            df,
            x=x,
            y=y,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

    # -----------------------------
    # HEATMAP
    # -----------------------------

    elif chart_type == "Correlation Heatmap":

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale=color_palette,
            template=template_style
        )

        st.plotly_chart(fig,use_container_width=True)

# -------------------------------
# COUNTRY COMPARISON
# -------------------------------
elif menu == "🌐 Country Comparison":

    st.markdown("<div class='title'>Country Comparison Dashboard</div>", unsafe_allow_html=True)

    country_cols = [c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col = country_cols[0]

        countries = st.multiselect(
            "Select Countries",
            df[country_col].unique(),
            default=df[country_col].unique()[:3]
        )

        if countries:

            filtered_df = df[df[country_col].isin(countries)]

            kpi_cols = st.multiselect(
                "Select KPIs",
                numeric_cols,
                default=numeric_cols[:3]
            )

            if kpi_cols:

                # ---------------- TABLE ----------------
                st.subheader("Comparison Table")
                st.dataframe(filtered_df[[country_col] + kpi_cols].reset_index(drop=True))

                # ---------------- BAR CHART ----------------
                st.subheader("📊 KPI Comparison")

                fig = px.bar(
                    filtered_df,
                    x=country_col,
                    y=kpi_cols,
                    barmode="group",
                    height=500,
                    template="plotly_dark"
                )

                st.plotly_chart(fig,use_container_width=True)

                # ---------------- LINE TREND ----------------
                year_cols=[c for c in df.columns if "year" in c.lower()]

                if year_cols:

                    year_col = year_cols[0]

                    st.subheader("📈 Country Trend Over Time")

                    fig2 = px.line(
                        filtered_df,
                        x=year_col,
                        y=kpi_cols,
                        color=country_col,
                        markers=True,
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig2,use_container_width=True)

                # ---------------- RADAR CHART ----------------
                if st.checkbox("Show Radar Chart"):

                    fig3 = go.Figure()

                    for c in countries:

                        country_data = filtered_df[filtered_df[country_col]==c][kpi_cols].mean()

                        fig3.add_trace(go.Scatterpolar(
                            r=country_data.values,
                            theta=kpi_cols,
                            fill='toself',
                            name=c
                        ))

                    fig3.update_layout(
                        polar=dict(radialaxis=dict(visible=True)),
                        title="Country Radar Comparison"
                    )

                    st.plotly_chart(fig3,use_container_width=True)

                # ---------------- SCATTER BUBBLE ----------------
                if len(kpi_cols) >= 2:

                    st.subheader("🫧 Bubble Relationship Chart")

                    fig4 = px.scatter(
                        filtered_df,
                        x=kpi_cols[0],
                        y=kpi_cols[1],
                        size=kpi_cols[0],
                        color=country_col,
                        hover_name=country_col,
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig4,use_container_width=True)

                # ---------------- BOX PLOT ----------------
                st.subheader("📦 Distribution Comparison")

                fig5 = px.box(
                    filtered_df,
                    x=country_col,
                    y=kpi_cols[0],
                    color=country_col,
                    template="plotly_dark"
                )

                st.plotly_chart(fig5,use_container_width=True)

                # ---------------- HEATMAP ----------------
                st.subheader("🔥 KPI Correlation Heatmap")

                corr = filtered_df[kpi_cols].corr()

                fig6 = px.imshow(
                    corr,
                    text_auto=True,
                    color_continuous_scale="RdBu",
                    template="plotly_dark"
                )

                st.plotly_chart(fig6,use_container_width=True)

                # ---------------- PARALLEL COORDINATES ----------------
                st.subheader("📊 Parallel Coordinates Analysis")

                fig7 = px.parallel_coordinates(
                    filtered_df,
                    dimensions=kpi_cols,
                    color=kpi_cols[0],
                    color_continuous_scale=px.colors.diverging.Tealrose
                )

                st.plotly_chart(fig7,use_container_width=True)

                # ---------------- AREA CHART ----------------
                st.subheader("📉 KPI Area Comparison")

                fig8 = px.area(
                    filtered_df,
                    x=country_col,
                    y=kpi_cols,
                    template="plotly_dark"
                )

                st.plotly_chart(fig8,use_container_width=True)

        else:
            st.info("Select at least one country.")

    else:
        st.warning("No country column found.")

# -------------------------------
# AI INSIGHTS GENERATOR
# -------------------------------
elif menu=="🤖 AI Insights Generator":

    st.title("🤖 AI Data Insights Engine")

    st.subheader("Dataset Statistical Summary")
    st.dataframe(df.describe())

    st.divider()

    st.subheader("📊 Automatic Statistical Insights")

    for col in numeric_cols:

        mean = df[col].mean()
        median = df[col].median()
        std = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()

        st.info(
            f"""
            🔹 **{col}**

            Mean Value: {mean:.2f}  
            Median Value: {median:.2f}  
            Standard Deviation: {std:.2f}  
            Minimum Value: {min_val:.2f}  
            Maximum Value: {max_val:.2f}
            """
        )

    st.divider()

    # -------------------------------
    # DISTRIBUTION VISUALIZATION
    # -------------------------------

    st.subheader("📈 Data Distribution Analysis")

    selected_col = st.selectbox("Select Column for Distribution", numeric_cols)

    fig = px.histogram(
        df,
        x=selected_col,
        nbins=30,
        color_discrete_sequence=["cyan"],
        title=f"{selected_col} Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.box(
        df,
        y=selected_col,
        title=f"{selected_col} Box Plot (Outlier Detection)"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # -------------------------------
    # CORRELATION INSIGHTS
    # -------------------------------

    st.subheader("🔥 Feature Correlation Insights")

    corr = df[numeric_cols].corr()

    fig3 = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig3, use_container_width=True)

    st.write("Strong correlations (>0.7 or <-0.7):")

    for col1 in numeric_cols:
        for col2 in numeric_cols:
            if col1 != col2:
                value = corr.loc[col1, col2]
                if abs(value) > 0.7:
                    st.success(f"{col1} and {col2} have strong correlation: {value:.2f}")

    st.divider()

    # -------------------------------
    # ANOMALY DETECTION
    # -------------------------------

    st.subheader("⚠ Automatic Outlier Detection")

    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower) | (df[col] > upper)]

        if len(outliers) > 0:
            st.warning(f"{col} contains {len(outliers)} potential outliers")

    st.divider()

    # -------------------------------
    # TOP & BOTTOM ANALYSIS
    # -------------------------------

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col = country_cols[0]

        st.subheader("🏆 Top Performing Countries")

        metric = st.selectbox("Select Metric", numeric_cols)

        top = df.sort_values(metric, ascending=False).head(10)

        fig4 = px.bar(
            top,
            x=metric,
            y=country_col,
            orientation="h",
            color=metric,
            title=f"Top Countries by {metric}"
        )

        st.plotly_chart(fig4, use_container_width=True)

        st.subheader("📉 Lowest Performing Countries")

        bottom = df.sort_values(metric).head(10)

        fig5 = px.bar(
            bottom,
            x=metric,
            y=country_col,
            orientation="h",
            color=metric,
            title=f"Lowest Countries by {metric}"
        )

        st.plotly_chart(fig5, use_container_width=True)

    st.divider()

    # -------------------------------
    # AI GENERATED TEXT INSIGHTS
    # -------------------------------

    st.subheader("🧠 Automated Insight Summary")

    for col in numeric_cols:

        mean = df[col].mean()
        std = df[col].std()

        if std > mean * 0.5:
            st.write(f"⚠ {col} shows high variability across countries.")
        else:
            st.write(f"✔ {col} values are relatively stable across the dataset.")

# -------------------------------
# COUNTRY ANALYSIS
# -------------------------------
elif menu=="🌍 Country Analysis":

    st.title("🌍 Country Analysis Dashboard")

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        country=st.selectbox("Select Country",df[country_col].unique())

        filtered=df[df[country_col]==country]

        st.subheader("Country Dataset")
        st.dataframe(filtered)

        st.divider()

        # ---------------- LINE CHART ----------------

        year_cols=[c for c in df.columns if "year" in c.lower()]

        if year_cols:

            year_col=year_cols[0]

            st.subheader("📈 Trend Over Time")

            fig2=px.line(
                filtered,
                x=year_col,
                y=numeric_cols,
                markers=True,
                template="plotly_dark",
                title="Income Trend Over Years"
            )

            st.plotly_chart(fig2,use_container_width=True)

        # ---------------- AREA CHART ----------------

        st.subheader("📉 Area Distribution")

        fig3=px.area(
            filtered,
            y=numeric_cols[0],
            template="plotly_dark",
            title="Income Distribution Area"
        )

        st.plotly_chart(fig3,use_container_width=True)

        # ---------------- PIE CHART ----------------

        st.subheader("🥧 Indicator Contribution")

        pie_df=filtered[numeric_cols].mean().reset_index()
        pie_df.columns=["Indicator","Value"]

        fig4=px.pie(
            pie_df,
            names="Indicator",
            values="Value",
            hole=0.4,
            template="plotly_dark"
        )

        st.plotly_chart(fig4,use_container_width=True)

        # ---------------- SCATTER PLOT ----------------

        if len(numeric_cols) >= 2:

            st.subheader("📉 Indicator Relationship")

            fig5=px.scatter(
                filtered,
                x=numeric_cols[0],
                y=numeric_cols[1],
                size=numeric_cols[0],
                color=numeric_cols[1],
                template="plotly_dark",
                title="Income Relationship Scatter"
            )

            st.plotly_chart(fig5,use_container_width=True)

        # ---------------- BOX PLOT ----------------

        st.subheader("📊 Distribution Analysis")

        fig6=px.box(
            filtered,
            y=numeric_cols,
            template="plotly_dark",
            title="Indicator Distribution"
        )

        st.plotly_chart(fig6,use_container_width=True)

        # ---------------- HEATMAP ----------------

        st.subheader("🔥 Correlation Heatmap")

        corr=filtered[numeric_cols].corr()

        fig7=px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu",
            title="Indicator Correlation",
            template="plotly_dark"
        )

        st.plotly_chart(fig7,use_container_width=True)

# -------------------------------
# GLOBAL MAP
# -------------------------------
elif menu=="🗺 Global Map Visualization":

    st.title("🌍 Global Income 3D Visualization")

    country_col = st.selectbox("Country Column", df.columns)
    value_col = st.selectbox("Value Column", numeric_cols)

    year_cols=[c for c in df.columns if "year" in c.lower()]

    st.subheader("3D Globe Income Visualization")

    # 3D globe style map
    fig = px.scatter_geo(
        df,
        locations=country_col,
        locationmode="country names",
        color=value_col,
        size=value_col,
        hover_name=country_col,
        projection="orthographic",
        color_continuous_scale="Turbo",
        title="Global Income Distribution"
    )

    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="rgb(15,15,20)",
            showocean=True,
            oceancolor="rgb(5,5,15)",
            showlakes=True,
            lakecolor="rgb(0,0,30)",
            showcountries=True,
            countrycolor="gray",
        ),
        paper_bgcolor="black",
        font=dict(color="white"),
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)


    # -------------------------------
    # 3D STYLE CHOROPLETH
    # -------------------------------

    st.subheader("Global Inequality Heatmap")

    fig2 = px.choropleth(
        df,
        locations=country_col,
        locationmode="country names",
        color=value_col,
        color_continuous_scale="Plasma",
        title="Global Inequality Distribution"
    )

    fig2.update_layout(
        geo=dict(
            projection_type="natural earth",
            showcountries=True,
            showcoastlines=True,
            showland=True,
            landcolor="rgb(30,30,40)"
        ),
        height=650
    )

    st.plotly_chart(fig2, use_container_width=True)


    # -------------------------------
    # GLOBAL TOP COUNTRIES CHART
    # -------------------------------

    st.subheader("Top Countries by Value")

    top_df = df.sort_values(value_col, ascending=False).head(10)

    fig3 = px.bar(
        top_df,
        x=value_col,
        y=country_col,
        orientation="h",
        color=value_col,
        color_continuous_scale="Turbo",
        title="Top 10 Countries"
    )

    fig3.update_layout(height=500)

    st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# MACHINE LEARNING
# -------------------------------
elif menu=="🧠 Machine Learning Prediction":

    st.title("🧠 Advanced Machine Learning Prediction")

    # Select Target
    target = st.selectbox("🎯 Select Target Variable", numeric_cols)

    features = [c for c in numeric_cols if c != target]

    X = df[features].fillna(0)
    y = df[target].fillna(0)

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Models
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(),
        "Gradient Boosting": GradientBoostingRegressor()
    }

    results = {}
    trained_models = {}

    st.subheader("⚙ Training Models")

    for name, model in models.items():

        model.fit(X_train, y_train)

        pred = model.predict(X_test)

        score = r2_score(y_test, pred)

        results[name] = score
        trained_models[name] = model

    results_df = pd.DataFrame(
        list(results.items()),
        columns=["Model", "R2 Score"]
    ).sort_values("R2 Score", ascending=False)

    # -------------------------------
    # MODEL PERFORMANCE TABLE
    # -------------------------------

    st.subheader("📊 Model Performance")

    st.dataframe(results_df)

    # -------------------------------
    # MODEL COMPARISON CHART
    # -------------------------------

    st.subheader("📈 Model Accuracy Comparison")

    fig = px.bar(
        results_df,
        x="Model",
        y="R2 Score",
        color="Model",
        title="Model Accuracy"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Best Model
    best_model_name = results_df.iloc[0]["Model"]

    st.success(f"🏆 Best Model Selected: {best_model_name}")

    best_model = trained_models[best_model_name]

    # -------------------------------
    # FEATURE IMPORTANCE
    # -------------------------------

    if best_model_name in ["Decision Tree","Random Forest","Gradient Boosting"]:

        st.subheader("🧠 Feature Importance")

        importance = best_model.feature_importances_

        imp_df = pd.DataFrame({
            "Feature": features,
            "Importance": importance
        }).sort_values("Importance", ascending=False)

        fig2 = px.bar(
            imp_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------
    # ACTUAL VS PREDICTED
    # -------------------------------

    st.subheader("📉 Actual vs Predicted")

    pred_test = best_model.predict(X_test)

    fig3 = px.scatter(
        x=y_test,
        y=pred_test,
        labels={"x":"Actual","y":"Predicted"},
        title="Actual vs Predicted Values"
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -------------------------------
    # RESIDUAL PLOT
    # -------------------------------

    st.subheader("📊 Residual Error Plot")

    residuals = y_test - pred_test

    fig4 = px.scatter(
        x=pred_test,
        y=residuals,
        labels={"x":"Predicted","y":"Residual Error"},
        title="Residual Plot"
    )

    st.plotly_chart(fig4, use_container_width=True)

    # -------------------------------
    # PREDICTION DISTRIBUTION
    # -------------------------------

    st.subheader("📈 Prediction Distribution")

    fig5 = px.histogram(
        pred_test,
        nbins=30,
        title="Distribution of Predicted Values"
    )

    st.plotly_chart(fig5, use_container_width=True)

    # -------------------------------
    # CORRELATION HEATMAP
    # -------------------------------

    st.subheader("🔥 Feature Correlation Heatmap")

    corr = df[features + [target]].corr()

    fig6 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation"
    )

    st.plotly_chart(fig6, use_container_width=True)

    # -------------------------------
    # USER INPUT PREDICTION
    # -------------------------------

    st.subheader("🔮 Make Prediction")

    user_inputs = []

    for col in features:

        val = st.number_input(
            f"Enter {col}",
            value=float(X[col].mean())
        )

        user_inputs.append(val)

    if st.button("🚀 Predict"):

        prediction = best_model.predict([user_inputs])[0]

        st.success(f"Predicted {target}: {prediction:.2f}")

# -------------------------------
# AUTO ML
# -------------------------------
elif menu=="⚡ Auto ML Prediction":

    st.title("⚡ Advanced Auto ML Model Selection")

    # Select target
    target = st.selectbox("🎯 Select Target Variable", numeric_cols)

    # Feature selection
    features = [c for c in numeric_cols if c != target]

    X = df[features]
    y = df[target]

    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Models
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(),
        "Gradient Boosting": GradientBoostingRegressor(),
        "KNN": KNeighborsRegressor()
    }

    results = {}
    predictions = {}

    st.subheader("🤖 Training Models...")

    for name, model in models.items():

        model.fit(X_train, y_train)

        pred = model.predict(X_test)

        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        rmse = np.sqrt(mean_squared_error(y_test, pred))

        results[name] = {
            "R2 Score": r2,
            "MAE": mae,
            "RMSE": rmse
        }

        predictions[name] = pred

    results_df = pd.DataFrame(results).T

    # -------------------------------
    # BEST MODEL
    # -------------------------------

    best_model = results_df["R2 Score"].idxmax()

    st.success(f"🏆 Best Model Selected: **{best_model}**")

    # -------------------------------
    # MODEL COMPARISON TABLE
    # -------------------------------

    st.subheader("📊 Model Performance Comparison")

    st.dataframe(results_df.style.highlight_max(axis=0))

    # -------------------------------
    # MODEL PERFORMANCE CHART
    # -------------------------------

    st.subheader("📈 Model Comparison Chart")

    fig = px.bar(
        results_df,
        y=results_df.index,
        x="R2 Score",
        orientation="h",
        title="Model Accuracy Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # ACTUAL VS PREDICTED
    # -------------------------------

    st.subheader("📉 Actual vs Predicted (Best Model)")

    best_pred = predictions[best_model]

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=y_test,
        y=best_pred,
        mode="markers",
        name="Predicted vs Actual"
    ))

    fig2.update_layout(
        xaxis_title="Actual Values",
        yaxis_title="Predicted Values",
        title="Prediction Accuracy"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------
    # FEATURE IMPORTANCE
    # -------------------------------

    if best_model in ["Decision Tree", "Random Forest", "Gradient Boosting"]:

        st.subheader("🧠 Feature Importance")

        model = models[best_model]

        importance = model.feature_importances_

        imp_df = pd.DataFrame({
            "Feature": features,
            "Importance": importance
        }).sort_values("Importance", ascending=False)

        fig3 = px.bar(
            imp_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Feature Importance"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # -------------------------------
    # DOWNLOAD PREDICTIONS
    # -------------------------------

    st.subheader("📥 Download Predictions")

    pred_df = pd.DataFrame({
        "Actual": y_test,
        "Predicted": best_pred
    })

    st.download_button(
        "Download CSV",
        pred_df.to_csv(index=False),
        file_name="predictions.csv"
    )

# -------------------------------
# TIME SERIES FORECASTING
# -------------------------------
elif menu=="⏳ Time Series Forecasting":

    st.title("⏳ Advanced Time Series Analysis & Forecast")

    time_col = st.selectbox("Time Column", df.columns)
    value_col = st.selectbox("Value Column", numeric_cols)

    # Sort data
    df_sorted = df.sort_values(time_col)

    # -------------------------------
    # ACTUAL TREND
    # -------------------------------

    st.subheader("📈 Actual Time Series Trend")

    fig = px.line(
        df_sorted,
        x=time_col,
        y=value_col,
        markers=True,
        title="Actual Data Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # MOVING AVERAGE
    # -------------------------------

    st.subheader("📊 Moving Average Trend")

    window = st.slider("Moving Average Window", 2, 10, 3)

    df_sorted["Moving_Avg"] = df_sorted[value_col].rolling(window).mean()

    fig2 = px.line(
        df_sorted,
        x=time_col,
        y=[value_col, "Moving_Avg"],
        title="Actual vs Moving Average Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------
    # FORECAST MODEL
    # -------------------------------

    st.subheader("🧠 Forecast Prediction")

    from sklearn.linear_model import LinearRegression
    import numpy as np

    try:
        df_sorted[time_col] = pd.to_numeric(df_sorted[time_col])
        X = df_sorted[[time_col]]
    except:
        df_sorted["time_numeric"] = np.arange(len(df_sorted))
        X = df_sorted[["time_numeric"]]

    y = df_sorted[value_col]

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    future_steps = st.slider("Forecast Steps", 1, 10, 5)

    last_val = X.iloc[-1, 0]

    future_x = np.arange(last_val + 1, last_val + future_steps + 1).reshape(-1, 1)

    forecast = model.predict(future_x)

    future_df = pd.DataFrame({
        time_col: future_x.flatten(),
        "Forecast": forecast
    })

    # -------------------------------
    # ACTUAL VS FORECAST
    # -------------------------------

    st.subheader("📉 Actual vs Forecast")

    fig3 = go.Figure()

    fig3.add_trace(go.Scatter(
        x=df_sorted[time_col],
        y=df_sorted[value_col],
        mode="lines+markers",
        name="Actual"
    ))

    fig3.add_trace(go.Scatter(
        x=future_df[time_col],
        y=future_df["Forecast"],
        mode="lines+markers",
        name="Forecast"
    ))

    fig3.update_layout(
        title="Forecasted Future Trend",
        xaxis_title=time_col,
        yaxis_title=value_col
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -------------------------------
    # CONFIDENCE BAND
    # -------------------------------

    st.subheader("📊 Forecast Confidence Range")

    std = y.std()

    upper = forecast + std
    lower = forecast - std

    fig4 = go.Figure()

    fig4.add_trace(go.Scatter(
        x=future_df[time_col],
        y=upper,
        line=dict(width=0),
        showlegend=False
    ))

    fig4.add_trace(go.Scatter(
        x=future_df[time_col],
        y=lower,
        fill='tonexty',
        name="Confidence Interval"
    ))

    fig4.add_trace(go.Scatter(
        x=future_df[time_col],
        y=forecast,
        mode="lines+markers",
        name="Forecast"
    ))

    st.plotly_chart(fig4, use_container_width=True)

    # -------------------------------
    # TREND INSIGHT
    # -------------------------------

    st.subheader("📊 Automatic Trend Insight")

    slope = model.coef_[0]

    if slope > 0:
        st.success("📈 The time series shows an upward trend.")
    elif slope < 0:
        st.warning("📉 The time series shows a downward trend.")
    else:
        st.info("➖ The time series appears stable.")

# -------------------------------
# PDF REPORT
# -------------------------------
elif menu=="📄 Generate PDF Report":
    st.title("Generate Report")
    if st.button("Create PDF"):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 750, "Global Income Report")
        pdf.drawString(100, 720, f"Rows: {df.shape[0]}")
        pdf.drawString(100, 700, f"Columns: {df.shape[1]}")
        pdf.save()
        buffer.seek(0)  # Important: reset buffer position before download
        st.download_button(
            label="Download PDF Report",
            data=buffer,
            file_name="Global_Income_Report.pdf",
            mime="application/pdf"
        )

# -------------------------------
# FAQ PAGE
# -------------------------------

elif menu == "❓ FAQ":

    st.markdown("<div class='title'>Frequently Asked Questions</div>", unsafe_allow_html=True)

    st.markdown("""
Welcome to the **FAQ section of the Global Income Intelligence Platform**.

This page answers common questions users may have while exploring the dashboard.  
It helps users understand how the platform works, how to interpret the analytics, and how to use the available tools effectively.
""")

    st.divider()

    with st.expander("What is the purpose of this platform?"):
        st.write("""
        The platform was created to analyze **global income inequality** using modern data analytics tools.

        It provides interactive dashboards that allow users to explore economic data, visualize inequality metrics,
        analyze country-level trends, and generate predictive insights using machine learning models.
        """)

    with st.expander("What dataset is used in this project?"):
        st.write("""
        The dashboard uses a global dataset containing information about income distribution across countries.

        Key variables include:

        • Country name  
        • Year  
        • Population statistics  
        • Gini Index  
        • Inequality Index  
        • Income distribution indicators
        """)

    with st.expander("What is the Gini Index?"):
        st.write("""
        The **Gini Index** is a widely used statistical measure of income inequality.

        A value of:

        • **0** represents perfect equality  
        • **100** represents maximum inequality  

        Countries with higher Gini Index values tend to have greater income disparity among citizens.
        """)

    with st.expander("What technologies power this dashboard?"):
        st.write("""
        The platform is built using a modern data analytics stack:

        • Python programming language  
        • Streamlit for interactive dashboards  
        • Pandas for data processing  
        • Plotly for visualizations  
        • Scikit-learn for machine learning  
        • ReportLab for PDF report generation
        """)

    with st.expander("Can this dashboard predict future inequality?"):
        st.write("""
        Yes. The platform includes machine learning modules that perform:

        • regression-based predictions  
        • forecasting of future inequality values  
        • trend analysis based on historical data

        These predictions provide insights into potential future patterns in global income distribution.
        """)

    with st.expander("Who can use this platform?"):
        st.write("""
        The platform is useful for a wide range of users including:

        • data analysts  
        • economists  
        • researchers  
        • students studying data science or economics  
        • policymakers evaluating economic inequality
        """)

    st.divider()

    st.info("If you still have questions, explore the Dashboard Guide section or review the About page for additional details.")


# -------------------------------
# ABOUT PLATFORM
# -------------------------------

elif menu == "ℹ About":

    st.markdown("<div class='title'>About the Global Income Intelligence Platform</div>", unsafe_allow_html=True)

    st.markdown("""

## Project Overview

The **Global Income Intelligence Platform** is an advanced data analytics dashboard designed to explore and analyze global income distribution patterns.

The platform integrates data visualization, statistical analysis, and machine learning models to transform complex economic datasets into meaningful insights.

Income inequality is a major global challenge that affects economic development, social stability, and policy decisions. This platform helps users understand these patterns by presenting data in an interactive and intuitive way.

---

## Project Objectives

The main objectives of this platform include:

• Visualizing global income inequality  
• Analyzing economic trends across countries  
• Providing interactive data exploration tools  
• Applying machine learning for predictive analytics  
• Generating automated analytical insights  

By combining these capabilities, the dashboard provides a powerful environment for exploring socioeconomic data.

---

## Key Features of the Platform

The platform includes several advanced analytics modules:

### Executive Dashboard
Provides a high-level overview of dataset statistics and inequality metrics.

### Dataset Explorer
Allows users to inspect raw data and analyze column statistics.

### Interactive Charts
Supports dynamic visualizations such as scatter plots, histograms, and line charts.

### Country Analysis
Enables country-level exploration of inequality indicators.

### Machine Learning Prediction
Uses regression models to estimate inequality values based on historical data.

### Forecasting Engine
Analyzes time-series trends to project future inequality patterns.

### Report Generation
Allows users to export analytical results as downloadable PDF reports.

---

## Technology Stack

This dashboard was developed using modern data science tools:

• **Python** – core programming language  
• **Streamlit** – dashboard development framework  
• **Pandas** – data manipulation and analysis  
• **Plotly** – interactive data visualizations  
• **Scikit-learn** – machine learning algorithms  
• **ReportLab** – PDF report generation  

Together these tools enable the development of scalable and interactive analytics platforms.

---

## Target Users

This platform can be used by:

• economists studying income inequality  
• researchers analyzing socioeconomic data  
• students learning data science and analytics  
• policymakers evaluating economic policies  
• analysts exploring global datasets

---

## Future Enhancements

Future improvements may include:

• real-time economic data integration  
• advanced machine learning forecasting models  
• AI-powered insight generation  
• interactive global 3D visualizations  
• cloud-based deployment

---

## Project Summary

The **Global Income Intelligence Platform** demonstrates how modern data analytics technologies can be applied to analyze complex global challenges such as income inequality.

By combining visualization, machine learning, and interactive dashboards, the platform transforms raw data into meaningful insights that support research and decision-making.

""")

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Platform Version", "1.0")
    col2.metric("Dashboard Modules", "10+")
    col3.metric("Visualization Types", "15+")
       






























