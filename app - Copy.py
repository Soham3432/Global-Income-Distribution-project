import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import shap
import openai
import requests
import boto3
from sqlalchemy import create_engine
from passlib.hash import bcrypt
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from fpdf import FPDF

st.set_page_config(layout="wide")

# ---------------- UI ----------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
color:white;
}

.kpi{
background:rgba(255,255,255,0.1);
padding:25px;
border-radius:18px;
text-align:center;
}

</style>
""",unsafe_allow_html=True)

# ---------------- DATABASE ----------------

DATABASE_URL="sqlite:///users.db"

engine=create_engine(DATABASE_URL)

def authenticate(username,password):

    users=pd.read_sql("SELECT * FROM users",engine)

    user=users[users.username==username]

    if len(user)>0:

        if bcrypt.verify(password,user.password_hash.values[0]):

            return True

    return False

# ---------------- LOGIN ----------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.title("Enterprise AI Analytics Platform")

    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Login"):

        if authenticate(u,p):

            st.session_state.login=True
            st.rerun()

        else:

            st.error("Invalid credentials")

    st.stop()

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df=load_data()

numeric_cols=df.select_dtypes(include=["int64","float64"]).columns

# ---------------- SIDEBAR ----------------

menu=st.sidebar.radio("Navigation",[

"Executive Dashboard",
"Power BI Dashboard",
"Dataset Explorer",
"Visualizations",
"AI Dataset Analyst",
"Automatic Insights",
"Explainable AI",
"Machine Learning",
"AutoML",
"Forecasting",
"3D Globe Map",
"AWS S3 Connector",
"Snowflake Connector",
"Live API Data",
"Streaming Dashboard",
"PDF Report",
"About"

])

# ---------------- EXECUTIVE DASHBOARD ----------------

if menu=="Executive Dashboard":

    c1,c2,c3=st.columns(3)

    c1.markdown(f"<div class='kpi'><h2>{df.shape[0]}</h2>Rows</div>",unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi'><h2>{df.shape[1]}</h2>Columns</div>",unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi'><h2>{len(numeric_cols)}</h2>Numeric</div>",unsafe_allow_html=True)

    st.dataframe(df.head())

# ---------------- POWER BI ----------------

elif menu=="Power BI Dashboard":

    url="YOUR_POWERBI_EMBED_LINK"

    st.components.v1.iframe(url,height=700)

# ---------------- VISUALIZATION ----------------

elif menu=="Visualizations":

    chart=st.selectbox("Chart",[

    "Histogram",
    "Scatter",
    "Box",
    "Violin",
    "Area",
    "Line"

    ])

    col=st.selectbox("Column",numeric_cols)

    fig=px.histogram(df,x=col)

    st.plotly_chart(fig)

# ---------------- AI ANALYST ----------------

elif menu=="AI Dataset Analyst":

    api=st.text_input("OpenAI API Key",type="password")

    q=st.text_input("Ask dataset question")

    if st.button("Ask"):

        openai.api_key=api

        prompt=f"Dataset columns: {list(df.columns)}. Question:{q}"

        response=openai.ChatCompletion.create(

        model="gpt-4o-mini",

        messages=[{"role":"user","content":prompt}]

        )

        st.write(response.choices[0].message.content)

# ---------------- AUTO INSIGHTS ----------------

elif menu=="Automatic Insights":

    for col in numeric_cols:

        st.write(

        f"{col} mean: {df[col].mean():.2f}, std: {df[col].std():.2f}"

        )

# ---------------- EXPLAINABLE AI ----------------

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

# ---------------- AUTOML ----------------

elif menu=="AutoML":

    target=st.selectbox("Target",numeric_cols)

    X=df[numeric_cols].drop(columns=[target])
    y=df[target]

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    models={

    "Linear":LinearRegression(),
    "Tree":DecisionTreeRegressor(),
    "Forest":RandomForestRegressor(),
    "GradientBoost":GradientBoostingRegressor(),
    "SVM":SVR(),
    "KNN":KNeighborsRegressor(),
    "Ridge":Ridge(),
    "Lasso":Lasso()

    }

    scores={}

    for name,m in models.items():

        m.fit(X_train,y_train)

        pred=m.predict(X_test)

        scores[name]=r2_score(y_test,pred)

    st.write(scores)

# ---------------- FORECASTING ----------------

elif menu=="Forecasting":

    date_col=st.selectbox("Date",df.columns)
    value_col=st.selectbox("Value",numeric_cols)

    data=df[[date_col,value_col]].dropna()

    data.columns=["ds","y"]

    model=Prophet()

    model.fit(data)

    future=model.make_future_dataframe(periods=365)

    forecast=model.predict(future)

    fig=model.plot(forecast)

    st.pyplot(fig)

# ---------------- 3D GLOBE ----------------

elif menu=="3D Globe Map":

    fig=go.Figure(go.Scattergeo())

    fig.update_layout(

    geo=dict(projection_type="orthographic")

    )

    st.plotly_chart(fig)

# ---------------- AWS S3 ----------------

elif menu=="AWS S3 Connector":

    bucket=st.text_input("S3 Bucket")

    if st.button("Load"):

        s3=boto3.client("s3")

        obj=s3.get_object(Bucket=bucket,Key="data.csv")

        df=pd.read_csv(obj["Body"])

        st.dataframe(df)

# ---------------- SNOWFLAKE ----------------

elif menu=="Snowflake Connector":

    conn=st.text_input("Snowflake Connection String")

    if st.button("Connect"):

        engine=create_engine(conn)

        data=pd.read_sql("SELECT * FROM table",engine)

        st.dataframe(data)

# ---------------- API ----------------

elif menu=="Live API Data":

    url=st.text_input("API URL")

    if st.button("Fetch"):

        r=requests.get(url)

        data=pd.DataFrame(r.json())

        st.dataframe(data)

# ---------------- STREAMING ----------------

elif menu=="Streaming Dashboard":

    st.write("Real-time streaming charts placeholder")

# ---------------- PDF ----------------

elif menu=="PDF Report":

    if st.button("Generate"):

        pdf=FPDF()

        pdf.add_page()

        pdf.set_font("Arial","B",16)

        pdf.cell(0,10,"Enterprise AI Report",ln=True)

        pdf.output("report.pdf")

        with open("report.pdf","rb") as f:

            st.download_button("Download",f,"report.pdf")

# ---------------- ABOUT ----------------

elif menu=="About":

    st.write("Enterprise AI Analytics Platform built with Streamlit.")
