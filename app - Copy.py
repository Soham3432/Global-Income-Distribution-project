import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# -------------------------------
# ADVANCED 3D UI STYLE
# -------------------------------
st.markdown("""
<style>
.stApp{
background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
color:white;
font-family: 'Segoe UI';
}
.title{
font-size:45px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#a855f7,#6366f1,#06b6d4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:25px;
transition: all 0.3s ease;
}
.card{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(12px);
border-radius:20px;
padding:25px;
box-shadow:0 10px 30px rgba(0,0,0,0.5);
transition: transform 0.3s ease, background 0.3s ease;
}
.card:hover{
transform: translateY(-10px) scale(1.03) rotateX(3deg) rotateY(3deg);
background: rgba(255,255,255,0.12);
}
.kpi-card{
background: linear-gradient(145deg,#1e1b4b,#312e81);
border-radius:18px;
padding:25px;
text-align:center;
box-shadow:0 12px 35px rgba(0,0,0,0.6);
transition: transform 0.3s ease, background 0.3s ease, color 0.3s ease;
cursor:pointer;
}
.kpi-card:hover{
transform: scale(1.08) rotateX(5deg) rotateY(5deg);
background: linear-gradient(145deg,#3b30a0,#5140c4);
color:#fff;
}
.kpi-number{
font-size:40px;
font-weight:800;
background: linear-gradient(90deg,#a78bfa,#06b6d4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
transition: all 0.3s ease;
}
.kpi-card:hover .kpi-number{
background: linear-gradient(90deg,#facc15,#22d3ee);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}
.kpi-label{
font-size:16px;
color:#ddd;
transition: color 0.3s ease;
}
.kpi-card:hover .kpi-label{
color:#fff;
}
section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#020617,#111827);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label{
transition: background 0.3s ease, color 0.3s ease;
border-radius: 10px;
padding: 5px 10px;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover{
background: linear-gradient(90deg,#6366f1,#a855f7,#06b6d4);
color:#fff;
transform: scale(1.05);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"]{
background: linear-gradient(90deg,#f59e0b,#22d3ee);
color:#fff;
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
# LOGIN SYSTEM
# -------------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("<div class='title'>🌍 Global Income Intelligence Platform</div>", unsafe_allow_html=True)
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid login")
    st.stop()

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go To",
    [
        "🏠 Introduction",
        "🏠 Executive Dashboard",
        "📘 Dashboard Guide",
        "📊 Power BI Dashboard",
        "🧾 Dataset Explorer",
        "📈 Chart Explorer",
        "🤖 AI Insights Generator",
        "🌍 Country Analysis",
        "🗺 Global Map Visualization",
        "🧠 Machine Learning Prediction",
        "⚡ Auto ML Prediction",
        "⏳ Time Series Forecasting",
        "📄 Generate PDF Report",
        "❓ FAQ",
        "ℹ About"
    ]
)

# -------------------------------
# INTRODUCTION SECTION
# -------------------------------
if menu == "🏠 Introduction":
    st.markdown("<div class='title'>Introduction</div>", unsafe_allow_html=True)

    st.markdown("""
### Project Title: Interactive Analytics Dashboard for Global Income Distribution

### Project Statement and Outcomes:
The Interactive Analytics Dashboard for Global Income Distribution project aims to develop an interactive Power BI dashboard that visualizes income inequality data across various countries and regions. This project involves collecting, preprocessing, and structuring global income distribution and economic data to enable effective visualization. 

The dashboard will provide users with insights into income disparities over time, country-wise comparisons, and patterns of inequality globally. The outcome will be a user-friendly dashboard, embedded within a Streamlit web application, offering an intuitive interface for economists, researchers, policymakers, and the general public. This platform will help users explore global income inequality, understand disparities across different regions, and analyze trends in wealth distribution. The project will conclude with comprehensive testing to ensure dashboard accuracy and usability, supported by detailed documentation for future reference and enhancements.
""", unsafe_allow_html=True)

    # Neomorphic KPI Cards
    st.markdown("""
    <style>
    .neo-card {
        background: #1e1e2f;
        border-radius: 15px;
        padding: 25px;
        margin: 10px 5px;
        color: white;
        text-align: center;
        box-shadow: 6px 6px 12px #161625, -6px -6px 12px #27283d;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        cursor: default;
        user-select: none;
        transition: box-shadow 0.3s ease;
    }
    .neo-card:hover {
        box-shadow: inset 6px 6px 12px #161625, inset -6px -6px 12px #27283d;
        color: #f0f8ff;
    }
    .neo-number {
        font-weight: 900;
        font-size: 40px;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #a78bfa, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .neo-label {
        font-weight: 600;
        font-size: 14px;
        color: #b0b7c3;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.markdown(f"""<div class="neo-card"><div class="neo-number">62.49</div><div class="neo-label">Inequality Range</div></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="neo-card"><div class="neo-number">37.52</div><div class="neo-label">Avg Gini Index</div></div>""", unsafe_allow_html=True)
    col3.markdown(f"""<div class="neo-card"><div class="neo-number">22.55</div><div class="neo-label">Avg Inequality Index</div></div>""", unsafe_allow_html=True)
    col4.markdown(f"""<div class="neo-card"><div class="neo-number">200</div><div class="neo-label">Total Countries</div></div>""", unsafe_allow_html=True)
    col5.markdown(f"""<div class="neo-card"><div class="neo-number">7.85bn</div><div class="neo-label">Total Updated Population</div></div>""", unsafe_allow_html=True)

# -------------------------------
# EXECUTIVE DASHBOARD
# -------------------------------
elif menu == "🏠 Executive Dashboard":
    st.markdown("<div class='title'>Executive Dashboard</div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.markdown(f"""<div class="kpi-card"><div class="kpi-number">{df.shape[0]}</div><div class="kpi-label">Total Rows</div></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="kpi-card"><div class="kpi-number">{df.shape[1]}</div><div class="kpi-label">Total Columns</div></div>""", unsafe_allow_html=True)
    col3.markdown(f"""<div class="kpi-card"><div class="kpi-number">{len(numeric_cols)}</div><div class="kpi-label">Numeric Features</div></div>""", unsafe_allow_html=True)
    col4.markdown(f"""<div class="kpi-card"><div class="kpi-number">{len(categorical_cols)}</div><div class="kpi-label">Categorical Features</div></div>""", unsafe_allow_html=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Insights")
    col1, col2 = st.columns(2)
    col1.markdown(f"""<div class="card"><h4>Missing Values</h4><p>{df.isnull().sum().sum()} missing values detected.</p></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="card"><h4>Duplicate Rows</h4><p>{df.duplicated().sum()} duplicate rows found.</p></div>""", unsafe_allow_html=True)

    if len(numeric_cols) > 0:
        fig, ax = plt.subplots()
        df[numeric_cols[0]].hist(ax=ax)
        st.pyplot(fig)

# -------------------------------
# (The rest of your existing sections: Dashboard Guide, Power BI, Dataset Explorer, etc.)
# -------------------------------
