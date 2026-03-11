import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import shap
import requests
import openai
from prophet import Prophet
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from sklearn.linear_model import (
LinearRegression,Ridge,Lasso,ElasticNet,
BayesianRidge,SGDRegressor,HuberRegressor,
PassiveAggressiveRegressor
)

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
RandomForestRegressor,
GradientBoostingRegressor,
ExtraTreesRegressor,
AdaBoostRegressor
)

from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense

from fpdf import FPDF
import io

st.set_page_config(layout="wide")

# ----------------------
# UI
# ----------------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
color:white;
}

.kpi{
background:rgba(255,255,255,0.08);
padding:25px;
border-radius:20px;
text-align:center;
}

</style>
""",unsafe_allow_html=True)

# ----------------------
# LOAD DATA
# ----------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df=load_data()

numeric_cols=df.select_dtypes(include=["int64","float64"]).columns

# ----------------------
# LOGIN
# ----------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.title("Global Income Intelligence Platform")

    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Login"):

        if u=="admin" and p=="1234":
            st.session_state.login=True
            st.rerun()

        else:
            st.error("Invalid Login")

    st.stop()

# ----------------------
# SIDEBAR
# ----------------------

menu=st.sidebar.radio("Navigation",[

"Executive Dashboard",
"Power BI Dashboard",
"Dataset Explorer",
"Chart Explorer",
"50+ Visualizations",
"3D Globe Map",
"AI Dataset Analyst",
"Explainable AI",
"Machine Learning",
"AutoML 15 Algorithms",
"Prophet Forecasting",
"LSTM Forecasting",
"SQL Database Connector",
"Live API Data",
"Auto Data Cleaning",
"PDF Report",
"FAQ",
"About"

])

# ----------------------
# EXECUTIVE DASHBOARD
# ----------------------

if menu=="Executive Dashboard":

    c1,c2,c3=st.columns(3)

    c1.markdown(f"<div class='kpi'><h2>{df.shape[0]}</h2>Rows</div>",unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'><h2>{df.shape[1]}</h2>Columns</div>",unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'><h2>{len(numeric_cols)}</h2>Numeric</div>",unsafe_allow_html=True)

    st.dataframe(df.head())

# ----------------------
# POWER BI
# ----------------------

elif menu=="Power BI Dashboard":

    powerbi_url="YOUR_POWERBI_LINK"

    st.components.v1.iframe(powerbi_url,height=700)

# ----------------------
# DATASET EXPLORER
# ----------------------

elif menu=="Dataset Explorer":

    st.dataframe(df)

# ----------------------
# 50+ VISUALIZATIONS
# ----------------------

elif menu=="50+ Visualizations":

    chart=st.selectbox("Chart",[

    "Histogram","Box","Scatter","Violin",
    "Area","Line","3D Scatter","Density"

    ])

    col=st.selectbox("Column",numeric_cols)

    if chart=="Histogram":

        fig=px.histogram(df,x=col)

    elif chart=="Box":

        fig=px.box(df,y=col)

    elif chart=="Violin":

        fig=px.violin(df,y=col)

    elif chart=="Area":

        fig=px.area(df,y=col)

    elif chart=="Line":

        fig=px.line(df,y=col)

    st.plotly_chart(fig)

# ----------------------
# 3D GLOBE
# ----------------------

elif menu=="3D Globe Map":

    fig=go.Figure(go.Scattergeo())

    fig.update_layout(

    geo=dict(
    projection_type="orthographic"
    )

    )

    st.plotly_chart(fig)

# ----------------------
# CHATGPT ANALYST
# ----------------------

elif menu=="AI Dataset Analyst":

    st.title("ChatGPT Data Analyst")

    api=st.text_input("OpenAI API Key",type="password")

    question=st.text_input("Ask about dataset")

    if st.button("Ask"):

        openai.api_key=api

        prompt=f"Dataset columns: {list(df.columns)}. Question: {question}"

        response=openai.ChatCompletion.create(

        model="gpt-4o-mini",

        messages=[

        {"role":"user","content":prompt}

        ]

        )

        st.write(response.choices[0].message.content)

# ----------------------
# EXPLAINABLE AI
# ----------------------

elif menu=="Explainable AI":

    target=st.selectbox("Target",numeric_cols)

    X=df[numeric_cols].drop(columns=[target])
    y=df[target]

    model=RandomForestRegressor()

    model.fit(X,y)

    explainer=shap.Explainer(model,X)

    shap_values=explainer(X)

    shap.summary_plot(shap_values,X,show=False)

    st.pyplot()

# ----------------------
# AUTOML
# ----------------------

elif menu=="AutoML 15 Algorithms":

    target=st.selectbox("Target",numeric_cols)

    X=df[numeric_cols].drop(columns=[target])
    y=df[target]

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    models={

    "Linear":LinearRegression(),
    "Ridge":Ridge(),
    "Lasso":Lasso(),
    "ElasticNet":ElasticNet(),
    "Bayesian":BayesianRidge(),
    "SGD":SGDRegressor(),
    "Huber":HuberRegressor(),
    "PassiveAggressive":PassiveAggressiveRegressor(),
    "Tree":DecisionTreeRegressor(),
    "RandomForest":RandomForestRegressor(),
    "ExtraTrees":ExtraTreesRegressor(),
    "GradientBoost":GradientBoostingRegressor(),
    "AdaBoost":AdaBoostRegressor(),
    "SVM":SVR(),
    "KNN":KNeighborsRegressor()

    }

    results={}

    for name,m in models.items():

        m.fit(X_train,y_train)

        pred=m.predict(X_test)

        results[name]=r2_score(y_test,pred)

    st.write(results)

# ----------------------
# LSTM FORECAST
# ----------------------

elif menu=="LSTM Forecasting":

    st.write("Deep learning forecasting module")

# ----------------------
# SQL CONNECTOR
# ----------------------

elif menu=="SQL Database Connector":

    db_url=st.text_input("Database URL")

    if st.button("Connect"):

        engine=create_engine(db_url)

        data=pd.read_sql("SELECT * FROM table_name",engine)

        st.dataframe(data)

# ----------------------
# API DATA
# ----------------------

elif menu=="Live API Data":

    url=st.text_input("API URL")

    if st.button("Load API Data"):

        r=requests.get(url)

        data=pd.DataFrame(r.json())

        st.dataframe(data)

# ----------------------
# CLEANING
# ----------------------

elif menu=="Auto Data Cleaning":

    clean=df.fillna(df.mean(numeric_only=True))

    st.dataframe(clean.head())

# ----------------------
# PDF
# ----------------------

elif menu=="PDF Report":

    if st.button("Generate"):

        pdf=FPDF()

        pdf.add_page()

        pdf.set_font("Arial","B",16)

        pdf.cell(0,10,"Income Report",ln=True)

        pdf.output("report.pdf")

        with open("report.pdf","rb") as f:

            st.download_button("Download",f,"report.pdf")

# ----------------------
# FAQ
# ----------------------

elif menu=="FAQ":

    st.write("FAQ Section")

# ----------------------
# ABOUT
# ----------------------

elif menu=="About":

    st.write("AI Data Science Platform built with Streamlit.")
