import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import shap
from prophet import Prophet
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
from fpdf import FPDF
import io

st.set_page_config(page_title="Global Income Intelligence Platform",layout="wide")

# -----------------------
# UI STYLE
# -----------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
color:white;
font-family:Segoe UI;
}

.title{
font-size:45px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#a855f7,#6366f1,#06b6d4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:20px;
}

.kpi-card{
background:linear-gradient(145deg,#1e1b4b,#312e81);
border-radius:18px;
padding:25px;
text-align:center;
box-shadow:0 10px 30px rgba(0,0,0,0.6);
transition:0.3s;
}

.kpi-card:hover{
transform:scale(1.05);
}

.kpi-number{
font-size:40px;
font-weight:800;
color:#a78bfa;
}

.kpi-label{
font-size:16px;
color:#ddd;
}

.card{
background:rgba(255,255,255,0.08);
padding:20px;
border-radius:20px;
backdrop-filter:blur(10px);
box-shadow:0 10px 30px rgba(0,0,0,0.4);
}

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#020617,#111827);
}

</style>
""",unsafe_allow_html=True)

# -----------------------
# LOAD DATA
# -----------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df=load_data()

numeric_cols=df.select_dtypes(include=["int64","float64"]).columns
categorical_cols=df.select_dtypes(include=["object"]).columns

# -----------------------
# LOGIN
# -----------------------

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

# -----------------------
# SIDEBAR
# -----------------------

st.sidebar.title("Navigation")

menu=st.sidebar.radio("Go To",[

"🏠 Executive Dashboard",
"📘 Dashboard Guide",
"📊 Power BI Dashboard",
"🧾 Dataset Explorer",
"📈 Chart Explorer",
"📊 Advanced Visualizations",
"🤖 AI Data Analyst",
"🧠 Explainable AI",
"🌍 Animated Global Map",
"🤖 AI Insights Generator",
"🌍 Country Analysis",
"🗺 Global Map Visualization",
"🧠 Machine Learning Prediction",
"⚡ Auto ML Prediction",
"📈 Advanced Forecasting",
"⏳ Time Series Forecasting",
"🎯 Auto Data Cleaning",
"📄 Generate Advanced PDF Report",
"❓ FAQ",
"ℹ About"

])

# -----------------------
# EXECUTIVE DASHBOARD
# -----------------------

if menu=="🏠 Executive Dashboard":

    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)

    c1.markdown(f"<div class='kpi-card'><div class='kpi-number'>{df.shape[0]}</div><div class='kpi-label'>Rows</div></div>",unsafe_allow_html=True)
    c2.markdown(f"<div class='kpi-card'><div class='kpi-number'>{df.shape[1]}</div><div class='kpi-label'>Columns</div></div>",unsafe_allow_html=True)
    c3.markdown(f"<div class='kpi-card'><div class='kpi-number'>{len(numeric_cols)}</div><div class='kpi-label'>Numeric</div></div>",unsafe_allow_html=True)
    c4.markdown(f"<div class='kpi-card'><div class='kpi-number'>{len(categorical_cols)}</div><div class='kpi-label'>Categorical</div></div>",unsafe_allow_html=True)

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    fig,ax=plt.subplots()

    if len(numeric_cols)>0:
        df[numeric_cols[0]].hist(ax=ax)
        st.pyplot(fig)

# -----------------------
# DASHBOARD GUIDE
# -----------------------

elif menu=="📘 Dashboard Guide":

    st.markdown("<div class='title'>Platform Guide</div>",unsafe_allow_html=True)

    st.markdown("""

### Executive Dashboard
Overview of dataset statistics and KPIs.

### Dataset Explorer
Explore raw dataset structure.

### Chart Explorer
Visualize relationships between variables.

### Advanced Visualizations
Explore 3D charts and interactive visuals.

### AI Data Analyst
Ask questions about the dataset.

### Explainable AI
Understand ML model feature importance.

### Global Map
Visualize income distribution across countries.

### Machine Learning
Predict numeric targets.

### Forecasting
Predict future trends.

### Auto Data Cleaning
Automatically fix missing values.

### PDF Report
Export professional reports.

""")

# -----------------------
# DATASET EXPLORER
# -----------------------

elif menu=="🧾 Dataset Explorer":

    st.title("Dataset Explorer")

    st.dataframe(df)

    column=st.selectbox("Column",df.columns)

    st.write(df[column].describe())

    st.write("Missing Values")

    st.write(df.isnull().sum())

# -----------------------
# CHART EXPLORER
# -----------------------

elif menu=="📈 Chart Explorer":

    st.title("Chart Explorer")

    chart=st.selectbox("Chart",["Histogram","Boxplot","Scatter","Heatmap"])

    fig,ax=plt.subplots()

    if chart=="Histogram":

        col=st.selectbox("Column",numeric_cols)

        sns.histplot(df[col],ax=ax)

    elif chart=="Boxplot":

        col=st.selectbox("Column",numeric_cols)

        sns.boxplot(x=df[col],ax=ax)

    elif chart=="Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)

        sns.scatterplot(x=df[x],y=df[y],ax=ax)

    elif chart=="Heatmap":

        sns.heatmap(df[numeric_cols].corr(),annot=True,ax=ax)

    st.pyplot(fig)

# -----------------------
# ADVANCED VISUALIZATION
# -----------------------

elif menu=="📊 Advanced Visualizations":

    st.title("Advanced Charts")

    chart=st.selectbox("Chart",["3D Scatter","Violin","Area"])

    if chart=="3D Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)
        z=st.selectbox("Z",numeric_cols)

        fig=px.scatter_3d(df,x=x,y=y,z=z)

        st.plotly_chart(fig)

    elif chart=="Violin":

        col=st.selectbox("Column",numeric_cols)

        fig=px.violin(df,y=col)

        st.plotly_chart(fig)

    elif chart=="Area":

        col=st.selectbox("Column",numeric_cols)

        fig=px.area(df,y=col)

        st.plotly_chart(fig)

# -----------------------
# AI DATA ANALYST
# -----------------------

elif menu=="🤖 AI Data Analyst":

    st.title("AI Data Analyst")

    q=st.text_input("Ask a dataset question")

    if q:

        if "average" in q:

            st.write(df.mean(numeric_only=True))

        elif "max" in q:

            st.write(df.max(numeric_only=True))

        else:

            st.write("Try asking about averages or max values.")

# -----------------------
# EXPLAINABLE AI
# -----------------------

elif menu=="🧠 Explainable AI":

    st.title("SHAP Explainable AI")

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

# -----------------------
# GLOBAL MAP
# -----------------------

elif menu=="🗺 Global Map Visualization":

    st.title("Global Map")

    country_col=st.selectbox("Country",df.columns)
    value_col=st.selectbox("Value",numeric_cols)

    fig=px.choropleth(df,locations=country_col,locationmode="country names",color=value_col)

    st.plotly_chart(fig)

# -----------------------
# ANIMATED MAP
# -----------------------

elif menu=="🌍 Animated Global Map":

    st.title("Animated Map")

    country=st.selectbox("Country Column",df.columns)
    value=st.selectbox("Value Column",numeric_cols)
    time=st.selectbox("Time Column",df.columns)

    fig=px.choropleth(df,locations=country,color=value,animation_frame=time)

    st.plotly_chart(fig)

# -----------------------
# MACHINE LEARNING
# -----------------------

elif menu=="🧠 Machine Learning Prediction":

    st.title("ML Prediction")

    target=st.selectbox("Target",numeric_cols)

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

        pred=model.predict([inputs])[0]

        st.success(pred)

# -----------------------
# AUTOML
# -----------------------

elif menu=="⚡ Auto ML Prediction":

    st.title("AutoML")

    target=st.selectbox("Target",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features]
    y=df[target]

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    models={

    "Linear":LinearRegression(),
    "Tree":DecisionTreeRegressor(),
    "Forest":RandomForestRegressor()

    }

    scores={}

    for name,m in models.items():

        m.fit(X_train,y_train)

        pred=m.predict(X_test)

        scores[name]=r2_score(y_test,pred)

    st.write(scores)

# -----------------------
# FORECASTING
# -----------------------

elif menu=="📈 Advanced Forecasting":

    st.title("Prophet Forecast")

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

# -----------------------
# CLEANING
# -----------------------

elif menu=="🎯 Auto Data Cleaning":

    st.title("Auto Cleaning")

    clean=df.fillna(df.mean(numeric_only=True))

    st.dataframe(clean.head())

# -----------------------
# PDF REPORT
# -----------------------

elif menu=="📄 Generate Advanced PDF Report":

    st.title("PDF Report")

    if st.button("Generate"):

        pdf=FPDF()

        pdf.add_page()

        pdf.set_font("Arial","B",16)

        pdf.cell(0,10,"Income Report",ln=True)

        pdf.cell(0,10,f"Rows: {df.shape[0]}",ln=True)

        pdf.output("report.pdf")

        with open("report.pdf","rb") as f:

            st.download_button("Download",f,"report.pdf")

# -----------------------
# FAQ
# -----------------------

elif menu=="❓ FAQ":

    st.write("Platform FAQ")

# -----------------------
# ABOUT
# -----------------------

elif menu=="ℹ About":

    st.write("Built using Python, Streamlit, Machine Learning and Plotly.")
