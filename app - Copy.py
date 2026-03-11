# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score
from prophet import Prophet
from fpdf import FPDF
import io
import shap
import requests
import openai

from sqlalchemy import create_engine, text
from passlib.hash import bcrypt

# ------------------ DATABASE SETUP ------------------
DATABASE_URL = "sqlite:///users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create users table and default admin if not exists
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            role TEXT
        )
    """))
    result = conn.execute(text("SELECT * FROM users WHERE username='admin'"))
    if result.fetchone() is None:
        password_hash = bcrypt.hash("admin123")
        conn.execute(text("""
            INSERT INTO users (username,password_hash,role)
            VALUES (:username,:password,:role)
        """), {"username":"admin","password":password_hash,"role":"admin"})
    conn.commit()

# ------------------ AUTHENTICATION ------------------
def authenticate(username,password):
    try:
        users = pd.read_sql("SELECT * FROM users", engine)
        user = users[users.username == username]
        if len(user) > 0 and bcrypt.verify(password, user.password_hash.values[0]):
            return True
    except Exception as e:
        st.error("Database error: "+str(e))
    return False

# ------------------ STREAMLIT APP ------------------
st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# Custom CSS for UI
st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:white;}
.kpi{background:rgba(255,255,255,0.08);padding:25px;border-radius:20px;text-align:center;}
.title{font-size:42px;font-weight:700;text-align:center;background: linear-gradient(90deg,#a855f7,#6366f1);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
</style>
""",unsafe_allow_html=True)

# ------------------ LOGIN ------------------
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:
    st.markdown("<div class='title'>🌍 Global Income Intelligence Platform</div>",unsafe_allow_html=True)
    user_input = st.text_input("Username")
    pw_input = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(user_input, pw_input):
            st.session_state.login=True
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()
numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# ------------------ SIDEBAR NAVIGATION ------------------
menu = st.sidebar.radio("Navigation", [
    "Executive Dashboard",
    "Power BI Dashboard",
    "Dataset Explorer",
    "Chart Explorer",
    "AI Insights Generator",
    "Country Analysis",
    "Global Map Visualization",
    "Machine Learning Prediction",
    "Auto ML Prediction",
    "Time Series Forecasting",
    "Generate PDF Report",
    "FAQ",
    "About"
])

# ------------------ EXECUTIVE DASHBOARD ------------------
if menu=="Executive Dashboard":
    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)
    col1,col2,col3=st.columns(3)
    col1.markdown(f"<div class='kpi'><h2>{df.shape[0]}</h2>Rows</div>",unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi'><h2>{df.shape[1]}</h2>Columns</div>",unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi'><h2>{len(numeric_cols)}</h2>Numeric</div>",unsafe_allow_html=True)
    st.subheader("Dataset Preview")
    st.dataframe(df.head())
    if len(numeric_cols)>0:
        fig,ax=plt.subplots()
        df[numeric_cols[0]].hist(ax=ax)
        st.pyplot(fig)

# ------------------ POWER BI ------------------
elif menu=="Power BI Dashboard":
    st.title("Power BI Dashboard")
    powerbi_url="YOUR_POWERBI_EMBED_LINK"
    st.components.v1.iframe(powerbi_url,height=700)

# ------------------ DATASET EXPLORER ------------------
elif menu=="Dataset Explorer":
    st.title("Dataset Explorer")
    st.dataframe(df)
    column = st.selectbox("Select Column",df.columns)
    st.write(df[column].describe())
    st.subheader("Missing Values")
    st.write(df.isnull().sum())
    st.subheader("Duplicate Rows")
    st.write(df.duplicated().sum())
    st.download_button("Download Dataset", df.to_csv(index=False), "dataset.csv")

# ------------------ CHART EXPLORER ------------------
elif menu=="Chart Explorer":
    st.title("Chart Explorer")
    chart = st.selectbox("Choose Chart", ["Histogram","Boxplot","Scatter","Bar","Line","Correlation Heatmap"])
    fig,ax=plt.subplots()
    if chart=="Histogram":
        col=st.selectbox("Column",numeric_cols)
        sns.histplot(df[col],ax=ax)
        explanation="Histogram shows distribution of values."
    elif chart=="Boxplot":
        col=st.selectbox("Column",numeric_cols)
        sns.boxplot(x=df[col],ax=ax)
        explanation="Boxplot shows median and outliers."
    elif chart=="Scatter":
        x=st.selectbox("X Axis",numeric_cols)
        y=st.selectbox("Y Axis",numeric_cols)
        sns.scatterplot(x=df[x],y=df[y],ax=ax)
        explanation="Scatter shows relationship between two variables."
    elif chart=="Bar":
        col=st.selectbox("Column",categorical_cols)
        df[col].value_counts().plot(kind="bar",ax=ax)
        explanation="Bar chart compares category frequencies."
    elif chart=="Line":
        col=st.selectbox("Column",numeric_cols)
        df[col].plot(ax=ax)
        explanation="Line chart shows trend across index."
    elif chart=="Correlation Heatmap":
        sns.heatmap(df[numeric_cols].corr(),annot=True,ax=ax)
        explanation="Heatmap shows correlation between numeric variables."
    st.pyplot(fig)
    st.info(explanation)

# ------------------ AI INSIGHTS GENERATOR ------------------
elif menu=="AI Insights Generator":
    st.title("Automatic AI Insights")
    st.subheader("Dataset Summary")
    st.write(df.describe())
    st.subheader("Generated Insights")
    for col in numeric_cols:
        mean=df[col].mean()
        median=df[col].median()
        std=df[col].std()
        st.info(f"{col}: Mean={mean:.2f} | Median={median:.2f} | Std Dev={std:.2f}")

# ------------------ COUNTRY ANALYSIS ------------------
elif menu=="Country Analysis":
    st.title("Country Analysis")
    country_cols=[c for c in df.columns if "country" in c.lower()]
    if country_cols:
        country_col=country_cols[0]
        country=st.selectbox("Select Country",df[country_col].unique())
        filtered=df[df[country_col]==country]
        st.dataframe(filtered)
        fig=px.bar(filtered,y=numeric_cols[0])
        st.plotly_chart(fig,use_container_width=True)

# ------------------ GLOBAL MAP ------------------
elif menu=="Global Map Visualization":
    st.title("Global Income Map")
    country_col=st.selectbox("Country Column",df.columns)
    value_col=st.selectbox("Value Column",numeric_cols)
    fig=px.choropleth(df, locations=country_col, locationmode="country names",
                      color=value_col, color_continuous_scale="Viridis")
    st.plotly_chart(fig,use_container_width=True)

# ------------------ ML PREDICTION ------------------
elif menu=="Machine Learning Prediction":
    st.title("Machine Learning Prediction")
    target=st.selectbox("Target Variable",numeric_cols)
    features=[c for c in numeric_cols if c!=target]
    X=df[features].fillna(0)
    y=df[target].fillna(0)
    model=LinearRegression()
    model.fit(X,y)
    inputs=[]
    for col in features:
        val=st.number_input(col,value=float(X[col].mean()))
        inputs.append(val)
    if st.button("Predict"):
        prediction=model.predict([inputs])[0]
        st.success(f"Predicted {target}: {prediction}")

# ------------------ AUTO ML ------------------
elif menu=="Auto ML Prediction":
    st.title("Auto ML Model Selection")
    target=st.selectbox("Target Variable",numeric_cols)
    features=[c for c in numeric_cols if c!=target]
    X=df[features]
    y=df[target]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    models={
        "Linear Regression":LinearRegression(),
        "Decision Tree":DecisionTreeRegressor(),
        "Random Forest":RandomForestRegressor()
    }
    results={}
    for name,model in models.items():
        model.fit(X_train,y_train)
        pred=model.predict(X_test)
        score=r2_score(y_test,pred)
        results[name]=score
    best=max(results,key=results.get)
    st.success(f"Best Model: {best}")
    st.write(results)

# ------------------ TIME SERIES ------------------
elif menu=="Time Series Forecasting":
    st.title("Time Series Analysis")
    time_col=st.selectbox("Time Column",df.columns)
    value_col=st.selectbox("Value Column",numeric_cols)
    df_sorted=df.sort_values(time_col)
    fig,ax=plt.subplots()
    ax.plot(df_sorted[time_col],df_sorted[value_col])
    ax.set_title("Trend Over Time")
    st.pyplot(fig)

# ------------------ PDF REPORT ------------------
elif menu=="Generate PDF Report":
    st.title("Generate Report")
    if st.button("Create PDF"):
        buffer=io.BytesIO()
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Arial","B",16)
        pdf.cell(0,10,"Global Income Report",ln=True)
        pdf.cell(0,10,f"Rows: {df.shape[0]}",ln=True)
        pdf.cell(0,10,f"Columns: {df.shape[1]}",ln=True)
        pdf.output(buffer)
        st.download_button("Download Report", buffer.getvalue(), "report.pdf", "application/pdf")

# ------------------ FAQ ------------------
elif menu=="FAQ":
    st.title("Frequently Asked Questions")
    st.markdown("""
**What does this platform do?**  
Provides analytics and machine learning insights for income datasets.

**What ML algorithms are used?**  
Linear Regression, Decision Tree, Random Forest.

**Can I visualize data?**  
Yes, multiple charts and maps are supported.

**Can I export reports?**  
Yes, PDF reports and dataset downloads are available.
""")

# ------------------ ABOUT ------------------
elif menu=="About":
    st.title("About Platform")
    st.write("""
Global Income Intelligence Platform built with:

• Python  
• Streamlit  
• Machine Learning  
• Plotly Visualization  
• Power BI Integration  
""")
