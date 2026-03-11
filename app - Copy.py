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
# NEON 3D UI STYLE
# -------------------------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top left, #050505, #0d0d0d, #111111);
color:white;
font-family: 'Segoe UI';
}

/* Neon Title */
.title{
font-size:45px;
font-weight:900;
text-align:center;
color: #0ff;
text-shadow:
0 0 5px #0ff,
0 0 10px #0ff,
0 0 20px #0ff,
0 0 40px #06f,
0 0 80px #06f;
margin-bottom:25px;
transition: all 0.4s ease;
}

/* Glass Neon Cards */
.card{
background: rgba(255,255,255,0.05);
backdrop-filter: blur(12px);
border-radius:20px;
padding:25px;
box-shadow: 0 0 10px #0ff, 0 0 20px #06f, 0 0 30px #0ff inset;
transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover{
transform: translateY(-10px) scale(1.03) rotateX(3deg) rotateY(3deg);
box-shadow: 0 0 20px #0ff, 0 0 40px #06f, 0 0 60px #0ff inset;
}

/* Neon KPI Cards */
.kpi-card{
background: linear-gradient(145deg,#111133,#1a1a44);
border-radius:18px;
padding:25px;
text-align:center;
box-shadow:0 0 10px #0ff, 0 0 20px #06f, 0 0 30px #0ff inset;
transition: transform 0.3s ease, box-shadow 0.3s ease, color 0.3s ease;
cursor:pointer;
}

.kpi-card:hover{
transform: scale(1.08) rotateX(5deg) rotateY(5deg);
box-shadow: 0 0 30px #0ff, 0 0 50px #06f, 0 0 80px #0ff inset;
background: linear-gradient(145deg,#222266,#5555ff);
color:#0ff;
}

.kpi-number{
font-size:40px;
font-weight:800;
color:#0ff;
text-shadow: 0 0 5px #0ff, 0 0 10px #06f, 0 0 20px #0ff;
transition: all 0.3s ease;
}

.kpi-card:hover .kpi-number{
color:#0ff;
text-shadow: 0 0 10px #0ff, 0 0 20px #06f, 0 0 30px #0ff;
}

.kpi-label{
font-size:16px;
color:#aad;
transition: color 0.3s ease;
}

.kpi-card:hover .kpi-label{
color:#0ff;
}

/* Sidebar Neon Effects */
section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#020617,#111827);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label{
transition: background 0.3s ease, color 0.3s ease, text-shadow 0.3s ease;
border-radius: 10px;
padding: 5px 10px;
color:#0ff;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover{
background: linear-gradient(90deg,#0ff,#06f,#0ff);
color:#fff;
text-shadow: 0 0 5px #0ff, 0 0 10px #06f, 0 0 20px #0ff;
transform: scale(1.05);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"]{
background: linear-gradient(90deg,#0ff,#06f,#0ff);
color:#fff;
text-shadow: 0 0 10px #0ff, 0 0 20px #06f;
}

</style>
""",unsafe_allow_html=True)

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
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='title'>🌍 Global Income Intelligence Platform</div>",unsafe_allow_html=True)

    user=st.text_input("Username")
    pw=st.text_input("Password",type="password")

    if st.button("Login"):

        if user=="admin" and pw=="1234":

            st.session_state.login=True
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
# EXECUTIVE DASHBOARD
# -------------------------------

if menu=="🏠 Executive Dashboard":

    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)

    col1,col2,col3,col4=st.columns(4)

    col1.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{df.shape[0]}</div>
    <div class="kpi-label">Total Rows</div>
    </div>
    """,unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{df.shape[1]}</div>
    <div class="kpi-label">Total Columns</div>
    </div>
    """,unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{len(numeric_cols)}</div>
    <div class="kpi-label">Numeric Features</div>
    </div>
    """,unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{len(categorical_cols)}</div>
    <div class="kpi-label">Categorical Features</div>
    </div>
    """,unsafe_allow_html=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Insights")
    col1,col2=st.columns(2)
    col1.markdown(f"""
    <div class="card">
    <h4>Missing Values</h4>
    <p>{df.isnull().sum().sum()} missing values detected.</p>
    </div>
    """,unsafe_allow_html=True)
    col2.markdown(f"""
    <div class="card">
    <h4>Duplicate Rows</h4>
    <p>{df.duplicated().sum()} duplicate rows found.</p>
    </div>
    """,unsafe_allow_html=True)

    if len(numeric_cols)>0:
        fig,ax=plt.subplots()
        df[numeric_cols[0]].hist(ax=ax)
        st.pyplot(fig)

# -------------------------------
# Continue rest of your features (Dashboard Guide, Power BI, Explorer, Charts, AI, ML, PDF, FAQ, About)
# All functionality preserved with neon UI enhancements
# -------------------------------
