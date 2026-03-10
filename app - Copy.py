import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# --------------------------------------------------
# WHITE MODERN UI STYLE
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background:white;
color:#1f2937;
font-family:'Segoe UI';
}

.main-title{
font-size:50px;
font-weight:800;
text-align:center;
color:#2563eb;
}

.card{
background:white;
padding:25px;
border-radius:14px;
border:1px solid #e5e7eb;
text-align:center;
box-shadow:0 5px 15px rgba(0,0,0,0.05);
}

.navbar{
background:#f9fafb;
padding:10px;
border-radius:10px;
margin-bottom:20px;
}

.logo{
font-size:26px;
font-weight:700;
color:#2563eb;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='main-title'>Global Income Intelligence Platform</div>",unsafe_allow_html=True)

    user=st.text_input("Username")
    pw=st.text_input("Password",type="password")

    if st.button("Login"):
        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

st.markdown("""
<div class='navbar'>
<div class='logo'>DataSphere Analytics Platform</div>
</div>
""", unsafe_allow_html=True)

menu = st.radio("",
[
"Dashboard",
"Upload Dataset",
"Chart Explorer",
"Statistics Lab",
"AI Insights",
"Correlation Analyzer",
"Auto Dashboard",
"Time Series Forecast",
"Machine Learning",
"Report Generator",
"FAQ"
],horizontal=True)

# --------------------------------------------------
# LOAD DEFAULT DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

if "data" not in st.session_state:
    st.session_state.data = load_data()

df = st.session_state.data

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if menu=="Dashboard":

    st.markdown("<div class='main-title'>Executive Dashboard</div>",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.markdown(f"<div class='card'><h2>{df.shape[0]}</h2>Total Records</div>",unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='card'><h2>{df.shape[1]}</h2>Total Columns</div>",unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div class='card'><h2>{len(numeric_cols)}</h2>Numeric Variables</div>",unsafe_allow_html=True)

    with c4:
        st.markdown(f"<div class='card'><h2>{len(categorical_cols)}</h2>Categorical Variables</div>",unsafe_allow_html=True)

    if len(numeric_cols)>0:

        fig = plt.figure()
        plt.hist(df[numeric_cols[0]], bins=30, color="blue")
        plt.title("Distribution Overview")
        plt.xlabel(numeric_cols[0])
        plt.ylabel("Frequency")
        st.pyplot(fig)

# --------------------------------------------------
# DATASET UPLOAD FEATURE
# --------------------------------------------------

elif menu=="Upload Dataset":

    st.title("Upload Your Dataset")

    file=st.file_uploader("Upload CSV",type=["csv"])

    if file:

        st.session_state.data=pd.read_csv(file)

        st.success("Dataset Loaded")

        st.dataframe(st.session_state.data)

# --------------------------------------------------
# CHART EXPLORER
# --------------------------------------------------

elif menu=="Chart Explorer":

    st.title("Chart Explorer")

    chart=st.selectbox("Chart Type",
    ["Bar","Pie","Line","Scatter"])

    if chart=="Bar":

        col=st.selectbox("Column",numeric_cols)

        fig=plt.figure()
        plt.bar(range(len(df[col])),df[col],color="yellow")
        plt.title("Bar Chart")
        st.pyplot(fig)

    elif chart=="Pie":

        col=st.selectbox("Category",categorical_cols)

        data=df[col].value_counts()

        fig=plt.figure()
        plt.pie(data.values,labels=data.index,colors=["yellow","blue","red","green"]) 
        plt.title("Pie Chart")
        st.pyplot(fig)

    elif chart=="Line":

        col=st.selectbox("Column",numeric_cols)

        fig=plt.figure()
        plt.plot(df[col],color="red")
        plt.title("Line Trend")
        st.pyplot(fig)

    elif chart=="Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)

        fig=plt.figure()
        plt.scatter(df[x],df[y],color="blue")
        plt.title("Scatter Relationship")
        st.pyplot(fig)

# --------------------------------------------------
# STATISTICS LAB
# --------------------------------------------------

elif menu=="Statistics Lab":

    st.title("Statistical Analysis")

    col=st.selectbox("Column",numeric_cols)

    st.write(df[col].describe())

    fig=plt.figure()
    plt.boxplot(df[col])
    plt.title("Boxplot Analysis")
    st.pyplot(fig)

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

elif menu=="AI Insights":

    st.title("Automated Data Insights")

    st.write("Dataset Shape:",df.shape)

    st.write("Missing Values")

    st.write(df.isnull().sum())

    st.write("Top Correlations")

    corr=df.corr(numeric_only=True)

    st.write(corr)

# --------------------------------------------------
# CORRELATION ANALYZER
# --------------------------------------------------

elif menu=="Correlation Analyzer":

    st.title("Correlation Heatmap")

    corr=df.corr(numeric_only=True)

    fig=plt.figure()
    plt.imshow(corr,cmap="coolwarm")
    plt.colorbar()
    plt.xticks(range(len(corr.columns)),corr.columns,rotation=90)
    plt.yticks(range(len(corr.columns)),corr.columns)

    st.pyplot(fig)

# --------------------------------------------------
# AUTO DASHBOARD
# --------------------------------------------------

elif menu=="Auto Dashboard":

    st.title("Automatic Chart Generator")

    for col in numeric_cols:

        fig=plt.figure()
        plt.hist(df[col],color="blue")
        plt.title(col)
        st.pyplot(fig)

# --------------------------------------------------
# TIME SERIES FORECAST
# --------------------------------------------------

elif menu=="Time Series Forecast":

    st.title("Forecasting Module")

    col=st.selectbox("Target Column",numeric_cols)

    df["time_index"]=range(len(df))

    X=df[["time_index"]]
    y=df[col]

    model=LinearRegression()

    model.fit(X,y)

    future=st.slider("Future Steps",1,50,10)

    future_index=np.arange(len(df),len(df)+future).reshape(-1,1)

    pred=model.predict(future_index)

    fig=plt.figure()

    plt.plot(df[col],color="blue")
    plt.plot(range(len(df),len(df)+future),pred,color="red")

    plt.title("Forecast")

    st.pyplot(fig)

# --------------------------------------------------
# MACHINE LEARNING
# --------------------------------------------------

elif menu=="Machine Learning":

    st.title("Prediction Model")

    target=st.selectbox("Target",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    model=RandomForestRegressor()

    model.fit(X,y)

    inputs=[]

    for col in features:

        val=st.number_input(col,value=float(X[col].mean()))

        inputs.append(val)

    if st.button("Predict"):

        pred=model.predict([inputs])[0]

        st.success(f"Predicted Value: {pred}")

        st.write("Model R2 Score:",r2_score(y,model.predict(X)))

# --------------------------------------------------
# REPORT GENERATOR
# --------------------------------------------------

elif menu=="Report Generator":

    if st.button("Generate PDF"):

        buffer=io.BytesIO()

        pdf=canvas.Canvas(buffer)

        pdf.drawString(100,750,"Income Analytics Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button("Download",buffer.getvalue(),"report.pdf")

# --------------------------------------------------
# FAQ
# --------------------------------------------------

elif menu=="FAQ":

    st.title("Platform Guide")

    st.write("""
This analytics platform allows users to explore datasets using
interactive visualizations, machine learning predictions,
and automated statistical insights.

Features include

• Dataset upload
• Chart explorer
• Statistical analysis
• AI insights
• Correlation analysis
• Automatic dashboards
• Forecasting models
• Machine learning predictions
• PDF report generation

This system is designed as a professional portfolio-level
analytics platform similar to enterprise BI tools.
""")
