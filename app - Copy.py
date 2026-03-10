import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# ---------------- GLOBAL STYLE ----------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#0f0229,#050012,#000000);
color:white;
font-family: 'Segoe UI';
}

.main-title{
font-size:50px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#8b5cf6,#22d3ee);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:18px;
box-shadow:0 0 30px rgba(139,92,246,0.4);
text-align:center;
transition:0.4s;
}

.card:hover{
transform:translateY(-8px) scale(1.02);
box-shadow:0 0 50px rgba(34,211,238,0.6);
}

.navbar{
background:rgba(255,255,255,0.05);
padding:12px;
border-radius:12px;
display:flex;
justify-content:space-around;
margin-bottom:20px;
}

.logo{
font-size:28px;
font-weight:700;
color:#a78bfa;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# ---------------- LOGIN ----------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='main-title'>🌍 Global Income Intelligence</div>",unsafe_allow_html=True)

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# ---------------- NAVIGATION ----------------

st.markdown("""
<div class='navbar'>
<span class='logo'>🚀 DataSphere</span>
</div>
""", unsafe_allow_html=True)

menu = st.radio(
"Navigation",
[
"🏠 Dashboard",
"📊 Chart Explorer",
"📈 Statistics Lab",
"🌍 Country Insights",
"🤖 ML Prediction",
"🔮 AI Forecast",
"📑 Generate Report",
"❓ FAQ"
],horizontal=True)

# ---------------- DASHBOARD ----------------

if menu=="🏠 Dashboard":

    st.markdown("<div class='main-title'>Executive Analytics Dashboard</div>",unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f"""<div class='card'>
        <h2>{df.shape[0]}</h2>
        <p>Total Records</p>
        </div>""",unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class='card'>
        <h2>{df.shape[1]}</h2>
        <p>Total Columns</p>
        </div>""",unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div class='card'>
        <h2>{len(numeric_cols)}</h2>
        <p>Numeric Variables</p>
        </div>""",unsafe_allow_html=True)

    with col4:
        st.markdown(f"""<div class='card'>
        <h2>{len(categorical_cols)}</h2>
        <p>Categorical Variables</p>
        </div>""",unsafe_allow_html=True)

    st.markdown("### Platform Overview")

    st.write("""
This platform provides advanced analytics capabilities for income datasets. 
Users can explore interactive charts, perform machine learning predictions, 
and analyze global income distribution patterns.

The dashboard includes 3D visualization tools, statistical exploration modules, 
and automated AI forecasting models that help identify trends, correlations, 
and predictive insights.
""")

    if len(numeric_cols)>1:

        fig = px.scatter_3d(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            z=numeric_cols[2] if len(numeric_cols)>2 else numeric_cols[0],
            color=numeric_cols[0],
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

# ---------------- CHART EXPLORER ----------------

elif menu=="📊 Chart Explorer":

    st.title("Interactive Chart Explorer")

    chart = st.selectbox("Choose Chart Type",[
        "3D Scatter",
        "3D Surface",
        "3D Line",
        "Bubble",
        "Pie",
        "Bar",
        "Line"
    ])

    if chart=="3D Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)
        z=st.selectbox("Z",numeric_cols)

        fig=px.scatter_3d(df,x=x,y=y,z=z,color=z,template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Surface":

        z=np.outer(df[numeric_cols[0]][:50],df[numeric_cols[1]][:50])
        fig=go.Figure(data=[go.Surface(z=z)])
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Line":

        fig=go.Figure()
        fig.add_trace(go.Scatter3d(
            x=df.index,
            y=df[numeric_cols[0]],
            z=df[numeric_cols[1]],
            mode='lines'
        ))

        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Bar":

        col=st.selectbox("Column",numeric_cols)
        fig=px.bar(df,y=col,template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Pie":

        col=st.selectbox("Category",categorical_cols)
        fig=px.pie(df,names=col,template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Line":

        col=st.selectbox("Column",numeric_cols)
        fig=px.line(df,y=col,template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

# ---------------- STATISTICS LAB ----------------

elif menu=="📈 Statistics Lab":

    st.title("Statistical Analysis")

    column=st.selectbox("Select Column",numeric_cols)

    st.write(df[column].describe())

    fig=px.histogram(df,x=column,nbins=40,template="plotly_dark")

    st.plotly_chart(fig,use_container_width=True)

# ---------------- COUNTRY INSIGHTS ----------------

elif menu=="🌍 Country Insights":

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        country=st.selectbox("Country",df[country_col].unique())

        data=df[df[country_col]==country]

        fig=px.bar(data,y=numeric_cols[0],template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

# ---------------- ML PREDICTION ----------------

elif menu=="🤖 ML Prediction":

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

# ---------------- FORECAST ----------------

elif menu=="🔮 AI Forecast":

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

    if st.button("Forecast"):
        pred=model.predict([inputs])[0]
        st.success(f"Forecast value: {pred}")

# ---------------- REPORT ----------------

elif menu=="📑 Generate Report":

    if st.button("Create PDF"):

        buffer=io.BytesIO()
        pdf=canvas.Canvas(buffer)

        pdf.drawString(100,750,"Income Intelligence Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button("Download",buffer.getvalue(),"report.pdf")

# ---------------- FAQ ----------------

elif menu=="❓ FAQ":

    st.title("Platform Guide")

    st.write("""
**What insights can be extracted?**

Users can analyze income distribution, detect correlations, 
and visualize multi-dimensional relationships using 3D analytics.

**What charts are supported?**

The system includes scatter plots, bubble charts, 3D surfaces, 
statistical histograms, correlation heatmaps, and interactive dashboards.

**What machine learning models are used?**

Linear Regression and Random Forest models are integrated 
to generate predictions and forecasting analytics.

**Who should use this platform?**

Data analysts, economists, and researchers who need 
interactive exploratory analytics for structured datasets.
""")
