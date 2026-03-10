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

# --------------------------------------------------
# GLOBAL ADVANCED UI STYLE
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#12002e,#070016,#000000);
color:white;
font-family:'Segoe UI';
}

.main-title{
font-size:55px;
font-weight:800;
text-align:center;
background:linear-gradient(90deg,#a855f7,#22d3ee,#6366f1);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.navbar{
background:rgba(255,255,255,0.05);
padding:12px;
border-radius:14px;
display:flex;
justify-content:center;
margin-bottom:20px;
box-shadow:0 0 20px rgba(168,85,247,0.4);
}

.logo{
font-size:30px;
font-weight:700;
color:#c084fc;
}

.card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:18px;
text-align:center;
box-shadow:0 0 35px rgba(168,85,247,0.4);
transition:0.4s;
}

.card:hover{
transform:translateY(-10px) scale(1.03);
box-shadow:0 0 60px rgba(34,211,238,0.6);
}

.section{
margin-top:40px;
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
# LOGIN SYSTEM
# --------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='main-title'>🌍 Global Income Intelligence Platform</div>",unsafe_allow_html=True)

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):

        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()

        else:
            st.error("Invalid Login")

    st.stop()

# --------------------------------------------------
# NAVBAR WEBSITE STYLE
# --------------------------------------------------

st.markdown("""
<div class='navbar'>
<span class='logo'>🚀 DataSphere Analytics</span>
</div>
""", unsafe_allow_html=True)

menu = st.radio(
"",
[
"🏠 Dashboard",
"📊 Power BI",
"📈 Chart Explorer",
"📊 Statistics Lab",
"🌍 World Analytics",
"🤖 AI Insights",
"🧠 Correlation AI",
"⚙ Auto Dashboard Builder",
"🔮 ML Prediction",
"📑 Report Generator",
"❓ FAQ"
],horizontal=True)

# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

if menu=="🏠 Dashboard":

    st.markdown("<div class='main-title'>Executive Analytics Dashboard</div>",unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.markdown(f"""<div class='card'>
        <h1>{df.shape[0]}</h1>
        <p>Total Records</p>
        </div>""",unsafe_allow_html=True)

    with col2:
        st.markdown(f"""<div class='card'>
        <h1>{df.shape[1]}</h1>
        <p>Total Columns</p>
        </div>""",unsafe_allow_html=True)

    with col3:
        st.markdown(f"""<div class='card'>
        <h1>{len(numeric_cols)}</h1>
        <p>Numeric Features</p>
        </div>""",unsafe_allow_html=True)

    with col4:
        st.markdown(f"""<div class='card'>
        <h1>{len(categorical_cols)}</h1>
        <p>Categorical Features</p>
        </div>""",unsafe_allow_html=True)

    st.markdown("### 3D Data Overview")

    if len(numeric_cols) > 2:

        fig = px.scatter_3d(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            z=numeric_cols[2],
            color=numeric_cols[0],
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# POWER BI DASHBOARD EMBED
# --------------------------------------------------

elif menu=="📊 Power BI":

    st.title("Embedded Power BI Dashboard")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# --------------------------------------------------
# CHART EXPLORER
# --------------------------------------------------

elif menu=="📈 Chart Explorer":

    st.title("Advanced Chart Explorer")

    chart = st.selectbox("Chart Type",[
        "3D Scatter",
        "3D Surface",
        "3D Line",
        "Bar",
        "Pie",
        "Line"
    ])

    if chart=="3D Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)
        z=st.selectbox("Z",numeric_cols)

        fig=px.scatter_3d(df,x=x,y=y,z=z,color=z,template="plotly_dark")
        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Surface":

        z=np.outer(df[numeric_cols[0]][:40],df[numeric_cols[1]][:40])

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

# --------------------------------------------------
# STATISTICS LAB
# --------------------------------------------------

elif menu=="📊 Statistics Lab":

    st.title("Statistical Analyzer")

    column = st.selectbox("Choose Column", numeric_cols)

    st.write(df[column].describe())

    fig = px.histogram(df,x=column,nbins=40,template="plotly_dark")

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# WORLD MAP ANALYTICS
# --------------------------------------------------

elif menu=="🌍 World Analytics":

    st.title("World Income Visualization")

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        metric=st.selectbox("Metric",numeric_cols)

        fig=px.choropleth(
            df,
            locations=country_col,
            locationmode="country names",
            color=metric,
            color_continuous_scale="Plasma"
        )

        st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# AI INSIGHTS GENERATOR
# --------------------------------------------------

elif menu=="🤖 AI Insights":

    st.title("Automated Data Insights")

    st.write("Dataset Shape:",df.shape)

    st.write("Missing Values:")

    st.write(df.isna().sum())

    st.write("Correlation Summary")

    st.write(df.corr(numeric_only=True))

# --------------------------------------------------
# CORRELATION AI
# --------------------------------------------------

elif menu=="🧠 Correlation AI":

    st.title("Correlation Explorer")

    corr=df.corr(numeric_only=True)

    fig=px.imshow(corr,text_auto=True,color_continuous_scale="Inferno")

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# AUTO DASHBOARD BUILDER
# --------------------------------------------------

elif menu=="⚙ Auto Dashboard Builder":

    st.title("Automatic Dashboard")

    for col in numeric_cols:

        fig=px.histogram(df,x=col,template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# ML PREDICTION
# --------------------------------------------------

elif menu=="🔮 ML Prediction":

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

# --------------------------------------------------
# REPORT GENERATOR
# --------------------------------------------------

elif menu=="📑 Report Generator":

    if st.button("Generate PDF Report"):

        buffer=io.BytesIO()

        pdf=canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Intelligence Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button("Download Report",buffer.getvalue(),"analytics_report.pdf")

# --------------------------------------------------
# FAQ
# --------------------------------------------------

elif menu=="❓ FAQ":

    st.title("Platform Documentation")

    st.write("""
This platform is an advanced analytics solution designed for interactive
exploration of global income datasets.

Users can explore charts, analyze correlations, generate automated dashboards,
and apply machine learning models to identify insights.

Key Capabilities

• Interactive 3D visualizations
• Embedded Power BI dashboards
• Automated AI insights
• Correlation analytics
• World income visualization
• Machine learning predictions
• Automatic dashboard generation
• PDF analytics reporting

The system is built using Streamlit, Plotly, Scikit-Learn and modern
web-style UI design to simulate enterprise analytics platforms like
Power BI, Tableau and modern SaaS analytics tools.
""")
