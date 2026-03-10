import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import time
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Global Income Intelligence", layout="wide")

# -----------------------------------------------------
# ADVANCED BLUE 3D UI
# -----------------------------------------------------

st.markdown("""
<style>

@keyframes glow {
0% {box-shadow:0 0 10px #0ea5e9;}
50% {box-shadow:0 0 30px #3b82f6;}
100% {box-shadow:0 0 10px #0ea5e9;}
}

.stApp{
background: radial-gradient(circle at top,#001233,#000814,#000000);
color:white;
font-family:Segoe UI;
}

.logo{
font-size:42px;
font-weight:800;
text-align:center;
background:linear-gradient(90deg,#0ea5e9,#3b82f6,#60a5fa);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:20px;
}

.card{
background:rgba(255,255,255,0.05);
border-radius:20px;
padding:25px;
backdrop-filter:blur(20px);
border:1px solid rgba(255,255,255,0.1);
animation:glow 4s infinite;
transition:0.4s;
}

.card:hover{
transform:scale(1.05) translateY(-5px);
}

.metric{
font-size:35px;
font-weight:700;
color:#60a5fa;
}

.sidebar .sidebar-content{
background:linear-gradient(#020617,#020617);
}

.stButton>button{
background:linear-gradient(90deg,#0ea5e9,#3b82f6);
border:none;
border-radius:10px;
padding:8px 25px;
color:white;
font-weight:600;
}

.stButton>button:hover{
box-shadow:0 0 20px #3b82f6;
transform:scale(1.05);
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='logo'>🌍 GLOBAL INCOME INTELLIGENCE</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns

# -----------------------------------------------------
# LOGIN
# -----------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.title("Secure Login")

    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Login"):

        if u=="admin" and p=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

menu = st.sidebar.selectbox("Navigation", [

"Executive Dashboard",
"3D Visual Analytics",
"Colorful 3D Charts",
"Advanced Charts",
"Real-Time Analytics",
"Machine Learning Prediction",
"Generate PDF Report",
"Dashboard Guide",
"Charts Explainer",
"FAQ",
"About"

])

# -----------------------------------------------------
# EXECUTIVE DASHBOARD
# -----------------------------------------------------

if menu=="Executive Dashboard":

    col1,col2,col3=st.columns(3)

    with col1:
        st.markdown(f"""
        <div class='card'>
        <h4>Total Rows</h4>
        <div class='metric'>{df.shape[0]}</div>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='card'>
        <h4>Total Columns</h4>
        <div class='metric'>{df.shape[1]}</div>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='card'>
        <h4>Numeric Variables</h4>
        <div class='metric'>{len(numeric_cols)}</div>
        </div>
        """,unsafe_allow_html=True)

    fig = px.histogram(
        df,
        x=numeric_cols[0],
        color_discrete_sequence=["#38bdf8"],
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

# -----------------------------------------------------
# 3D VISUAL ANALYTICS
# -----------------------------------------------------

elif menu=="3D Visual Analytics":

    st.title("3D Data Explorer")

    x=st.selectbox("X Axis",numeric_cols)
    y=st.selectbox("Y Axis",numeric_cols)
    z=st.selectbox("Z Axis",numeric_cols)

    fig = go.Figure(data=[go.Scatter3d(
        x=df[x],
        y=df[y],
        z=df[z],
        mode='markers',
        marker=dict(
            size=6,
            color=df[z],
            colorscale="Turbo",
            opacity=0.9
        )
    )])

    fig.update_layout(
        template="plotly_dark",
        scene=dict(
        bgcolor="#020617"
        )
    )

    st.plotly_chart(fig,use_container_width=True)

# -----------------------------------------------------
# COLORFUL 3D CHARTS
# -----------------------------------------------------

elif menu=="Colorful 3D Charts":

    chart=st.selectbox("Choose 3D Chart",[
    "3D Surface",
    "3D Mesh",
    "3D Volume",
    "3D Spiral"
    ])

    if chart=="3D Surface":

        x=np.linspace(-5,5,80)
        y=np.linspace(-5,5,80)

        X,Y=np.meshgrid(x,y)

        Z=np.sin(np.sqrt(X**2+Y**2))

        fig=go.Figure(data=[go.Surface(
        z=Z,
        colorscale="Rainbow"
        )])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Mesh":

        fig=go.Figure(data=[go.Mesh3d(
        x=np.random.randn(100),
        y=np.random.randn(100),
        z=np.random.randn(100),
        color='cyan',
        opacity=0.6
        )])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Volume":

        X,Y,Z=np.mgrid[-5:5:30j,-5:5:30j,-5:5:30j]

        values=np.sin(X*Y*Z)

        fig=go.Figure(data=go.Volume(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=values.flatten(),
        opacity=0.1,
        surface_count=15,
        colorscale="Plasma"
        ))

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Spiral":

        t=np.linspace(0,10,1000)

        x=np.sin(t)
        y=np.cos(t)
        z=t

        fig=go.Figure(data=[go.Scatter3d(
        x=x,y=y,z=z,
        mode='lines',
        line=dict(color=t,colorscale="Turbo",width=8)
        )])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

# -----------------------------------------------------
# ADVANCED CHARTS
# -----------------------------------------------------

elif menu=="Advanced Charts":

    fig = px.scatter(
    df,
    x=numeric_cols[0],
    y=numeric_cols[1],
    size=numeric_cols[0],
    color=numeric_cols[1],
    color_continuous_scale="Turbo",
    template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

# -----------------------------------------------------
# REAL TIME DATA
# -----------------------------------------------------

elif menu=="Real-Time Analytics":

    st.title("Real-Time Streaming Dashboard")

    chart=st.line_chart(np.random.randn(20,3))

    for i in range(40):
        chart.add_rows(np.random.randn(1,3))
        time.sleep(0.15)

# -----------------------------------------------------
# MACHINE LEARNING
# -----------------------------------------------------

elif menu=="Machine Learning Prediction":

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

    if st.button("Predict"):

        pred=model.predict([inputs])[0]

        st.success(f"Prediction: {pred}")

# -----------------------------------------------------
# PDF REPORT
# -----------------------------------------------------

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

# -----------------------------------------------------
# DASHBOARD GUIDE
# -----------------------------------------------------

elif menu=="Dashboard Guide":

    st.markdown("""

### Dashboard Usage Guide

Executive Dashboard → dataset overview  

3D Visual Analytics → explore relationships  

Colorful 3D Charts → advanced scientific visuals  

Real-Time Analytics → simulated streaming data  

Machine Learning → prediction models  

""")

# -----------------------------------------------------
# CHART EXPLAINER
# -----------------------------------------------------

elif menu=="Charts Explainer":

    st.markdown("""

### Chart Explanation

**3D Surface**
Shows terrain-like data relationships.

**Mesh 3D**
Displays complex 3D geometry.

**Volume Plot**
Represents density within 3D space.

**Spiral 3D**
Demonstrates dynamic data flows.

""")

# -----------------------------------------------------
# FAQ
# -----------------------------------------------------

elif menu=="FAQ":

    st.markdown("""

**Q: What dataset is used?**  
Income distribution dataset.

**Q: Which visualization library is used?**  
Plotly interactive charts.

**Q: Can I connect live data?**  
Yes using APIs or streaming services.

""")

# -----------------------------------------------------
# ABOUT
# -----------------------------------------------------

elif menu=="About":

    st.markdown("""

### Global Income Intelligence Platform

Features

• Blue neon 3D UI  
• Interactive 3D analytics  
• AI prediction models  
• Real-time dashboards  
• PDF report generation  

Built using **Streamlit + Plotly + Machine Learning**

""")
