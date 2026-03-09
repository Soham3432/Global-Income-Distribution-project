import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import time
import io

st.set_page_config(page_title="Enterprise Data Intelligence Platform", layout="wide")

# --------------------------------------------------
# GLASSMORPHISM UI
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#050018,#0d0030,#1b0048);
color:white;
font-family:Segoe UI;
}

.title{
font-size:48px;
font-weight:800;
text-align:center;
background:linear-gradient(90deg,#a855f7,#6366f1);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.card{
background:rgba(255,255,255,0.05);
backdrop-filter:blur(15px);
padding:20px;
border-radius:20px;
box-shadow:0 10px 40px rgba(0,0,0,0.7);
}

.stButton>button{
background:linear-gradient(90deg,#7c3aed,#6366f1);
border:none;
border-radius:10px;
padding:8px 25px;
color:white;
}

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#0a0028,#130044);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='title'>🌍 Enterprise Data Intelligence</div>",unsafe_allow_html=True)

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):

        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# --------------------------------------------------
# FILTER PANEL
# --------------------------------------------------

st.sidebar.title("🎛️ Data Filters")

filtered_df = df.copy()

for col in categorical_cols[:3]:

    values = st.sidebar.multiselect(col, df[col].unique())

    if values:
        filtered_df = filtered_df[filtered_df[col].isin(values)]

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

menu = st.sidebar.selectbox("Navigation",[

"Live KPI Dashboard",
"3D Globe Map",
"Animated Analytics",
"Auto Anomaly Detection",
"Auto ML Prediction",
"AI Data Analyst",
"Power BI Dashboard",
"Generate PDF Report",
"About"

])

# --------------------------------------------------
# LIVE KPI STREAMING
# --------------------------------------------------

if menu=="Live KPI Dashboard":

    st.markdown("<div class='title'>⚡ Live KPI Dashboard</div>",unsafe_allow_html=True)

    kpi1,kpi2,kpi3 = st.columns(3)

    placeholder1 = kpi1.empty()
    placeholder2 = kpi2.empty()
    placeholder3 = kpi3.empty()

    for i in range(10):

        placeholder1.metric("Total Records", filtered_df.shape[0] + np.random.randint(-5,5))
        placeholder2.metric("Avg Value", round(filtered_df[numeric_cols[0]].mean()+np.random.random(),2))
        placeholder3.metric("Max Value", filtered_df[numeric_cols[0]].max()+np.random.randint(-2,2))

        time.sleep(1)

# --------------------------------------------------
# 3D GLOBE MAP
# --------------------------------------------------

elif menu=="3D Globe Map":

    st.title("🌍 Global 3D Map")

    country_cols=[c for c in filtered_df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        fig = px.choropleth(
            filtered_df,
            locations=country_col,
            locationmode="country names",
            color=numeric_cols[0],
            color_continuous_scale="plasma",
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    else:
        st.warning("Country column not detected")

# --------------------------------------------------
# ANIMATED ANALYTICS
# --------------------------------------------------

elif menu=="Animated Analytics":

    st.title("📊 Animated Data Visualization")

    x = st.selectbox("X Axis", numeric_cols)
    y = st.selectbox("Y Axis", numeric_cols)

    fig = px.scatter(
        filtered_df,
        x=x,
        y=y,
        size=numeric_cols[0],
        color=numeric_cols[0],
        animation_frame=filtered_df.index,
        color_continuous_scale="turbo",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# ANOMALY DETECTION
# --------------------------------------------------

elif menu=="Auto Anomaly Detection":

    st.title("📈 AI Anomaly Detection")

    model = IsolationForest()

    X = filtered_df[numeric_cols].fillna(0)

    preds = model.fit_predict(X)

    filtered_df["Anomaly"] = preds

    fig = px.scatter(
        filtered_df,
        x=numeric_cols[0],
        y=numeric_cols[1],
        color="Anomaly",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# AUTO ML
# --------------------------------------------------

elif menu=="Auto ML Prediction":

    st.title("🧠 Auto Machine Learning")

    target = st.selectbox("Target Variable", numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=filtered_df[features].fillna(0)
    y=filtered_df[target].fillna(0)

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    models={
    "LinearRegression":LinearRegression(),
    "RandomForest":RandomForestRegressor(),
    "DecisionTree":DecisionTreeRegressor()
    }

    scores={}

    for name,model in models.items():

        model.fit(X_train,y_train)

        preds=model.predict(X_test)

        scores[name]=r2_score(y_test,preds)

    best=max(scores,key=scores.get)

    st.success(f"Best Model: {best}")

# --------------------------------------------------
# AI DATA ANALYST
# --------------------------------------------------

elif menu=="AI Data Analyst":

    st.title("🤖 AI Data Analyst")

    question = st.text_input("Ask about the dataset")

    if question:

        st.write("Dataset shape:", filtered_df.shape)

        for col in numeric_cols[:3]:

            st.write(f"{col} mean:", round(filtered_df[col].mean(),2))

# --------------------------------------------------
# POWER BI
# --------------------------------------------------

elif menu=="Power BI Dashboard":

    st.title("Power BI Dashboard")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# --------------------------------------------------
# PDF REPORT
# --------------------------------------------------

elif menu=="Generate PDF Report":

    st.title("Generate Analytics Report")

    if st.button("Create PDF"):

        buffer = io.BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.drawString(100,750,"Enterprise Analytics Report")
        pdf.drawString(100,720,f"Rows: {filtered_df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {filtered_df.shape[1]}")

        pdf.save()

        st.download_button(
            "Download PDF",
            buffer.getvalue(),
            "report.pdf",
            "application/pdf"
        )

# --------------------------------------------------
# ABOUT
# --------------------------------------------------

elif menu=="About":

    st.write("""
Enterprise Data Intelligence Platform.

Features:

• 3D global map analytics  
• animated dashboards  
• AI anomaly detection  
• auto machine learning  
• live KPI streaming  
• AI data assistant  
• Power BI integration  
• automated PDF reports
""")
