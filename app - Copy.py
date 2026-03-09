import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from reportlab.pdfgen import canvas
import numpy as np
import io

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# ---------------------------------------------------
# GLOBAL STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#09001f,#14003d,#24005f);
color:white;
font-family: 'Segoe UI';
}

.title{
font-size:45px;
font-weight:700;
text-align:center;
background: linear-gradient(90deg,#a855f7,#6366f1);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.metric{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:15px;
text-align:center;
box-shadow:0 10px 40px rgba(0,0,0,0.7);
}

.stButton>button{
background:linear-gradient(90deg,#7c3aed,#6366f1);
border:none;
border-radius:10px;
padding:8px 25px;
color:white;
}

</style>
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

    st.markdown("<div class='title'>🌍 Global Income Intelligence</div>",unsafe_allow_html=True)

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
# SIDEBAR
# ---------------------------------------------------

menu = st.sidebar.selectbox("Navigation",[

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

    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Numeric Variables", len(numeric_cols))

    if len(numeric_cols)>0:

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

    st.title("Power BI Dashboard")

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

    st.title("Advanced Plotly Visualizations")

    chart = st.selectbox("Choose Chart",[
        "3D Scatter",
        "Animated Scatter",
        "Bubble Chart",
        "Radar Chart",
        "Correlation Heatmap",
        "3D Surface"
    ])

    if chart=="3D Scatter":

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)
        z = st.selectbox("Z Axis", numeric_cols)

        fig = go.Figure(data=[go.Scatter3d(
            x=df[x],
            y=df[y],
            z=df[z],
            mode='markers',
            marker=dict(
                size=6,
                color=df[z],
                colorscale='Plasma',
                opacity=0.8
            )
        )])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Animated Scatter":

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.scatter(
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

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.scatter(
            df,
            x=x,
            y=y,
            size=numeric_cols[0],
            color=numeric_cols[0],
            hover_data=df.columns,
            color_continuous_scale="Rainbow",
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Radar Chart":

        sample = df[numeric_cols].mean()

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=sample.values,
            theta=sample.index,
            fill='toself'
        ))

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Correlation Heatmap":

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Inferno",
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Surface":

        z = np.outer(df[numeric_cols[0]][:50], df[numeric_cols[1]][:50])

        fig = go.Figure(data=[go.Surface(z=z, colorscale='Viridis')])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# COUNTRY ANALYSIS
# ---------------------------------------------------

elif menu=="Country Analysis":

    st.title("Country Analysis")

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        country = st.selectbox("Select Country", df[country_col].unique())

        filtered = df[df[country_col]==country]

        st.dataframe(filtered)

        fig = px.bar(
            filtered,
            y=numeric_cols[0],
            color_discrete_sequence=["#6366f1"],
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# ML PREDICTION
# ---------------------------------------------------

elif menu=="Machine Learning Prediction":

    st.title("Machine Learning Prediction")

    target = st.selectbox("Target Variable", numeric_cols)

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

# ---------------------------------------------------
# AI FORECAST
# ---------------------------------------------------

elif menu=="AI Forecasting":

    st.title("AI Forecasting")

    target = st.selectbox("Target Variable", numeric_cols)

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

        prediction=model.predict([inputs])[0]

        st.success(f"Forecasted {target}: {prediction}")

# ---------------------------------------------------
# PDF REPORT
# ---------------------------------------------------

elif menu=="Generate PDF Report":

    st.title("Generate Report")

    if st.button("Create PDF"):

        buffer = io.BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Report")
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

    st.write("""
Advanced analytics platform for **income distribution dataset**.

Features:
• 3D data visualizations  
• Animated charts  
• Machine learning prediction  
• AI forecasting  
• Embedded Power BI  
• PDF analytics report
""")
