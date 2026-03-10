import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from reportlab.pdfgen import canvas
import numpy as np
import io

st.set_page_config(page_title="Global Income Intelligence", layout="wide")

# ---------------------------------------------------
# ADVANCED 3D UI STYLE
# ---------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&display=swap');

html, body, [class*="css"]  {
font-family: 'Orbitron', sans-serif;
}

.stApp{
background: radial-gradient(circle at top,#0f0030,#050010,#000000);
color:white;
}

header {visibility: hidden;}

# --------------------------
# LOGO HEADER
# --------------------------

.logo{
font-size:40px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#8b5cf6,#22d3ee);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:20px;
}

.subtitle{
text-align:center;
color:#a1a1aa;
margin-bottom:30px;
}

# --------------------------
# GLASS CARDS
# --------------------------

.card{
background: rgba(255,255,255,0.05);
backdrop-filter: blur(20px);
border-radius:20px;
padding:25px;
box-shadow:0 20px 60px rgba(0,0,0,0.7);
transition:0.4s;
border:1px solid rgba(255,255,255,0.1);
}

.card:hover{
transform: translateY(-8px) scale(1.02);
box-shadow:0 30px 80px rgba(0,0,0,0.9);
}

.metric-big{
font-size:35px;
font-weight:700;
color:#a855f7;
}

.metric-title{
color:#aaa;
}

# --------------------------
# SIDEBAR
# --------------------------

section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#07001a,#020009);
border-right:1px solid rgba(255,255,255,0.05);
}

.stButton>button{
background:linear-gradient(90deg,#7c3aed,#22d3ee);
border:none;
padding:10px 25px;
border-radius:12px;
color:white;
font-weight:600;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.05);
box-shadow:0 0 20px #8b5cf6;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOGO HEADER
# ---------------------------------------------------

st.markdown("""
<div class='logo'>🌍 GLOBAL INCOME INTELLIGENCE</div>
<div class='subtitle'>Advanced AI Powered Data Analytics Platform</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# ---------------------------------------------------
# LOGIN SYSTEM
# ---------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("### Secure Login")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):

        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------

st.sidebar.title("🚀 Navigation")

menu = st.sidebar.radio("Go to",[
"Executive Dashboard",
"Power BI Dashboard",
"Dataset Explorer",
"Advanced Charts",
"Country Analysis",
"Machine Learning Prediction",
"AI Forecasting",
"Generate PDF Report",
"About"
])

# ---------------------------------------------------
# EXECUTIVE DASHBOARD
# ---------------------------------------------------

if menu=="Executive Dashboard":

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class='card'>
        <div class='metric-title'>Rows</div>
        <div class='metric-big'>{df.shape[0]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
        <div class='metric-title'>Columns</div>
        <div class='metric-big'>{df.shape[1]}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='card'>
        <div class='metric-title'>Numeric Variables</div>
        <div class='metric-big'>{len(numeric_cols)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Distribution Analysis")

    fig = px.histogram(
        df,
        x=numeric_cols[0],
        nbins=40,
        color_discrete_sequence=["#8b5cf6"],
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# POWER BI
# ---------------------------------------------------

elif menu=="Power BI Dashboard":

    st.title("Power BI Analytics")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# ---------------------------------------------------
# DATASET EXPLORER
# ---------------------------------------------------

elif menu=="Dataset Explorer":

    st.title("Dataset Explorer")

    st.dataframe(df)

    column = st.selectbox("Select Column", df.columns)

    st.write(df[column].describe())

# ---------------------------------------------------
# ADVANCED CHARTS
# ---------------------------------------------------

elif menu=="Advanced Charts":

    chart = st.selectbox("Choose Chart",[
    "3D Scatter",
    "Animated Scatter",
    "Bubble Chart",
    "Radar Chart",
    "Correlation Heatmap",
    "3D Surface"
    ])

    if chart=="3D Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)
        z=st.selectbox("Z",numeric_cols)

        fig=go.Figure(data=[go.Scatter3d(
            x=df[x],
            y=df[y],
            z=df[z],
            mode='markers',
            marker=dict(size=6,color=df[z],colorscale='Plasma')
        )])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Animated Scatter":

        x=st.selectbox("X Axis",numeric_cols)
        y=st.selectbox("Y Axis",numeric_cols)

        fig=px.scatter(
            df,
            x=x,
            y=y,
            size=numeric_cols[0],
            color=numeric_cols[0],
            animation_frame=df.index,
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Bubble Chart":

        x=st.selectbox("X Axis",numeric_cols)
        y=st.selectbox("Y Axis",numeric_cols)

        fig=px.scatter(
            df,
            x=x,
            y=y,
            size=numeric_cols[0],
            color=numeric_cols[0],
            color_continuous_scale="Rainbow",
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Radar Chart":

        sample=df[numeric_cols].mean()

        fig=go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=sample.values,
            theta=sample.index,
            fill='toself'
        ))

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Correlation Heatmap":

        corr=df[numeric_cols].corr()

        fig=px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Inferno",
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Surface":

        z=np.outer(df[numeric_cols[0]][:50],df[numeric_cols[1]][:50])

        fig=go.Figure(data=[go.Surface(z=z)])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# COUNTRY ANALYSIS
# ---------------------------------------------------

elif menu=="Country Analysis":

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        country=st.selectbox("Select Country",df[country_col].unique())

        filtered=df[df[country_col]==country]

        st.dataframe(filtered)

        fig=px.bar(
            filtered,
            y=numeric_cols[0],
            color_discrete_sequence=["#6366f1"],
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# MACHINE LEARNING
# ---------------------------------------------------

elif menu=="Machine Learning Prediction":

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

        st.success(f"Prediction: {pred}")

# ---------------------------------------------------
# AI FORECAST
# ---------------------------------------------------

elif menu=="AI Forecasting":

    target=st.selectbox("Target Variable",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    model=RandomForestRegressor()
    model.fit(X,y)

    inputs=[]

    for col in features:
        val=st.number_input(col,value=float(X[col].mean()))
        inputs.append(val)

    if st.button("Forecast"):

        pred=model.predict([inputs])[0]

        st.success(f"Forecast: {pred}")

# ---------------------------------------------------
# PDF REPORT
# ---------------------------------------------------

elif menu=="Generate PDF Report":

    if st.button("Create PDF"):

        buffer=io.BytesIO()

        pdf=canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Intelligence Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button(
        "Download PDF",
        buffer.getvalue(),
        "report.pdf",
        "application/pdf"
        )

# ---------------------------------------------------
# ABOUT
# ---------------------------------------------------

elif menu=="About":

    st.markdown("""
### Global Income Intelligence Platform

Features:

• 3D visualizations  
• AI forecasting  
• Machine learning prediction  
• PowerBI embedded analytics  
• Interactive dashboards  
• Automated PDF reports  

Built with **Streamlit + Plotly + AI models**
""")
