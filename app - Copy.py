import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import shap
from prophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
from fpdf import FPDF
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense
import io

st.set_page_config(page_title="Global Income Intelligence Platform",layout="wide")

# -----------------------------
# FUTURISTIC UI
# -----------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
color:white;
font-family:Segoe UI;
}

.title{
font-size:46px;
font-weight:900;
text-align:center;
background: linear-gradient(90deg,#a855f7,#6366f1,#06b6d4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.kpi{
background:rgba(255,255,255,0.08);
padding:25px;
border-radius:20px;
text-align:center;
box-shadow:0 10px 40px rgba(0,0,0,0.6);
transition:0.3s;
}

.kpi:hover{
transform:scale(1.05);
}

</style>
""",unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df=load_data()

numeric_cols=df.select_dtypes(include=["int64","float64"]).columns
categorical_cols=df.select_dtypes(include=["object"]).columns

# -----------------------------
# LOGIN
# -----------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='title'>🌍 Global Income Intelligence Platform</div>",unsafe_allow_html=True)

    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Login"):

        if u=="admin" and p=="1234":

            st.session_state.login=True
            st.rerun()

        else:
            st.error("Invalid Login")

    st.stop()

# -----------------------------
# SIDEBAR
# -----------------------------

menu=st.sidebar.radio("Navigation",[

"Executive Dashboard",
"Dashboard Guide",
"Power BI Dashboard",
"Dataset Explorer",
"Chart Explorer",
"Advanced Visualizations",
"3D Globe Map",
"AI Data Analyst",
"Explainable AI",
"Country Analysis",
"Global Map",
"Animated Map",
"Machine Learning Prediction",
"AutoML (10 Algorithms)",
"LSTM Forecasting",
"Prophet Forecasting",
"Auto Data Cleaning",
"PDF Report",
"FAQ",
"About"

])

# -----------------------------
# EXECUTIVE DASHBOARD
# -----------------------------

if menu=="Executive Dashboard":

    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)

    c1.markdown(f"<div class='kpi'><h2>{df.shape[0]}</h2>Rows</div>",unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'><h2>{df.shape[1]}</h2>Columns</div>",unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'><h2>{len(numeric_cols)}</h2>Numeric</div>",unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi'><h2>{len(categorical_cols)}</h2>Categorical</div>",unsafe_allow_html=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# -----------------------------
# DASHBOARD GUIDE
# -----------------------------

elif menu=="Dashboard Guide":

    st.title("Platform Guide")

    st.markdown("""

Executive Dashboard → dataset overview

Power BI Dashboard → enterprise BI report

Dataset Explorer → inspect dataset

Chart Explorer → quick visual analysis

Advanced Visualizations → 3D charts

AI Data Analyst → ask dataset questions

Explainable AI → SHAP interpretation

AutoML → multiple ML models

Forecasting → future predictions

""")

# -----------------------------
# POWER BI EMBED
# -----------------------------

elif menu=="Power BI Dashboard":

    st.title("Power BI Embedded Dashboard")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# -----------------------------
# DATASET EXPLORER
# -----------------------------

elif menu=="Dataset Explorer":

    st.dataframe(df)

    col=st.selectbox("Column",df.columns)

    st.write(df[col].describe())

# -----------------------------
# CHART EXPLORER
# -----------------------------

elif menu=="Chart Explorer":

    chart=st.selectbox("Chart",["Histogram","Scatter","Boxplot","Heatmap"])

    fig,ax=plt.subplots()

    if chart=="Histogram":

        c=st.selectbox("Column",numeric_cols)

        sns.histplot(df[c],ax=ax)

    elif chart=="Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)

        sns.scatterplot(x=df[x],y=df[y],ax=ax)

    elif chart=="Boxplot":

        c=st.selectbox("Column",numeric_cols)

        sns.boxplot(x=df[c],ax=ax)

    elif chart=="Heatmap":

        sns.heatmap(df[numeric_cols].corr(),annot=True,ax=ax)

    st.pyplot(fig)

# -----------------------------
# ADVANCED VISUALIZATION
# -----------------------------

elif menu=="Advanced Visualizations":

    chart=st.selectbox("Chart",[

    "3D Scatter",
    "Violin",
    "Area",
    "Treemap",
    "Sunburst"

    ])

    if chart=="3D Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)
        z=st.selectbox("Z",numeric_cols)

        fig=px.scatter_3d(df,x=x,y=y,z=z)

        st.plotly_chart(fig)

# -----------------------------
# 3D GLOBE
# -----------------------------

elif menu=="3D Globe Map":

    st.title("3D Globe")

    fig=go.Figure(go.Scattergeo())

    fig.update_layout(

    geo=dict(
        projection_type="orthographic"
    )

    )

    st.plotly_chart(fig)

# -----------------------------
# AI ANALYST
# -----------------------------

elif menu=="AI Data Analyst":

    q=st.text_input("Ask dataset question")

    if q:

        if "average" in q:

            st.write(df.mean(numeric_only=True))

        elif "max" in q:

            st.write(df.max(numeric_only=True))

        else:

            st.write("Try asking about averages or maximum values.")

# -----------------------------
# SHAP
# -----------------------------

elif menu=="Explainable AI":

    target=st.selectbox("Target",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features]
    y=df[target]

    model=RandomForestRegressor()

    model.fit(X,y)

    explainer=shap.Explainer(model,X)

    shap_values=explainer(X)

    shap.summary_plot(shap_values,X,show=False)

    st.pyplot()

# -----------------------------
# GLOBAL MAP
# -----------------------------

elif menu=="Global Map":

    country=st.selectbox("Country Column",df.columns)
    value=st.selectbox("Value",numeric_cols)

    fig=px.choropleth(df,locations=country,locationmode="country names",color=value)

    st.plotly_chart(fig)

# -----------------------------
# ANIMATED MAP
# -----------------------------

elif menu=="Animated Map":

    country=st.selectbox("Country",df.columns)
    value=st.selectbox("Value",numeric_cols)
    time=st.selectbox("Time",df.columns)

    fig=px.choropleth(df,locations=country,color=value,animation_frame=time)

    st.plotly_chart(fig)

# -----------------------------
# ML
# -----------------------------

elif menu=="Machine Learning Prediction":

    target=st.selectbox("Target",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features]
    y=df[target]

    model=LinearRegression()

    model.fit(X,y)

    st.success("Model trained")

# -----------------------------
# AUTOML
# -----------------------------

elif menu=="AutoML (10 Algorithms)":

    target=st.selectbox("Target",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features]
    y=df[target]

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    models={

    "Linear":LinearRegression(),
    "Tree":DecisionTreeRegressor(),
    "Forest":RandomForestRegressor(),
    "GB":GradientBoostingRegressor(),
    "SVM":SVR(),
    "KNN":KNeighborsRegressor()

    }

    scores={}

    for name,m in models.items():

        m.fit(X_train,y_train)

        pred=m.predict(X_test)

        scores[name]=r2_score(y_test,pred)

    st.write(scores)

# -----------------------------
# LSTM
# -----------------------------

elif menu=="LSTM Forecasting":

    st.write("LSTM forecasting module placeholder")

# -----------------------------
# PROPHET
# -----------------------------

elif menu=="Prophet Forecasting":

    date=st.selectbox("Date",df.columns)
    value=st.selectbox("Value",numeric_cols)

    data=df[[date,value]].dropna()

    data.columns=["ds","y"]

    model=Prophet()

    model.fit(data)

    future=model.make_future_dataframe(periods=365)

    forecast=model.predict(future)

    fig=model.plot(forecast)

    st.pyplot(fig)

# -----------------------------
# CLEANING
# -----------------------------

elif menu=="Auto Data Cleaning":

    clean=df.fillna(df.mean(numeric_only=True))

    st.dataframe(clean.head())

# -----------------------------
# PDF
# -----------------------------

elif menu=="PDF Report":

    if st.button("Generate"):

        pdf=FPDF()

        pdf.add_page()

        pdf.set_font("Arial","B",16)

        pdf.cell(0,10,"Income Report",ln=True)

        pdf.cell(0,10,f"Rows: {df.shape[0]}",ln=True)

        pdf.output("report.pdf")

        with open("report.pdf","rb") as f:

            st.download_button("Download",f,"report.pdf")

# -----------------------------
# FAQ
# -----------------------------

elif menu=="FAQ":

    st.write("FAQ section")

# -----------------------------
# ABOUT
# -----------------------------

elif menu=="About":

    st.write("Built using Streamlit, ML, Plotly, Power BI")
