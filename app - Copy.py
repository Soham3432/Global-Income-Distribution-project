import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Intelligence Platform", layout="wide")

# --------------------------------------------------
# ULTRA GLASSMORPHISM UI
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#070020,#120038,#1b0052);
color:white;
font-family:Segoe UI;
}

.title{
font-size:48px;
font-weight:800;
text-align:center;
background:linear-gradient(90deg,#a855f7,#6366f1);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.card{
background:rgba(255,255,255,0.05);
backdrop-filter:blur(15px);
padding:20px;
border-radius:18px;
box-shadow:0 10px 40px rgba(0,0,0,0.7);
}

.stButton>button{
background:linear-gradient(90deg,#7c3aed,#6366f1);
border:none;
border-radius:12px;
padding:10px 25px;
color:white;
}

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#0a0028,#130044);
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
# LOGIN
# --------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='title'>🌍 Global Intelligence Platform</div>",unsafe_allow_html=True)

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):

        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# --------------------------------------------------
# PROFESSIONAL FILTER PANEL
# --------------------------------------------------

st.sidebar.title("🎛️ Global Filters")

filtered_df = df.copy()

for col in categorical_cols[:3]:

    values = st.sidebar.multiselect(col, df[col].unique())

    if values:
        filtered_df = filtered_df[filtered_df[col].isin(values)]

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

menu = st.sidebar.selectbox("Navigation",[

"Executive Dashboard",
"3D World Map",
"Animated Time Series",
"Advanced Charts",
"AI Insights",
"Auto ML Prediction",
"Power BI Dashboard",
"Generate PDF Report",
"About"

])

# --------------------------------------------------
# EXECUTIVE DASHBOARD
# --------------------------------------------------

if menu=="Executive Dashboard":

    st.markdown("<div class='title'>Executive Analytics</div>",unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Rows", filtered_df.shape[0])

    with col2:
        st.metric("Columns", filtered_df.shape[1])

    with col3:
        st.metric("Numeric Variables", len(numeric_cols))

    if len(numeric_cols)>0:

        fig = px.histogram(
            filtered_df,
            x=numeric_cols[0],
            color_discrete_sequence=["#a855f7"],
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# 3D WORLD MAP
# --------------------------------------------------

elif menu=="3D World Map":

    st.title("🌍 Global Income Map")

    if "country" in [c.lower() for c in filtered_df.columns]:

        country_col=[c for c in filtered_df.columns if "country" in c.lower()][0]

        fig = px.choropleth(
            filtered_df,
            locations=country_col,
            locationmode="country names",
            color=numeric_cols[0],
            color_continuous_scale="plasma",
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    else:
        st.warning("No country column found.")

# --------------------------------------------------
# ANIMATED TIME SERIES
# --------------------------------------------------

elif menu=="Animated Time Series":

    st.title("📊 Animated Data Growth")

    x = st.selectbox("X Axis", numeric_cols)
    y = st.selectbox("Y Axis", numeric_cols)

    fig = px.scatter(
        filtered_df,
        x=x,
        y=y,
        size=numeric_cols[0],
        color=numeric_cols[0],
        animation_frame=filtered_df.index,
        color_continuous_scale="turbo",
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# ADVANCED CHARTS
# --------------------------------------------------

elif menu=="Advanced Charts":

    st.title("📈 Advanced Data Visualizations")

    chart = st.selectbox("Chart Type",[
        "3D Scatter",
        "Bubble Chart",
        "Radar Chart",
        "Correlation Heatmap",
        "3D Surface"
    ])

    if chart=="3D Scatter":

        x = st.selectbox("X", numeric_cols)
        y = st.selectbox("Y", numeric_cols)
        z = st.selectbox("Z", numeric_cols)

        fig = go.Figure(data=[go.Scatter3d(
            x=filtered_df[x],
            y=filtered_df[y],
            z=filtered_df[z],
            mode='markers',
            marker=dict(size=6,color=filtered_df[z],colorscale='plasma')
        )])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Bubble Chart":

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.scatter(
            filtered_df,
            x=x,
            y=y,
            size=numeric_cols[0],
            color=numeric_cols[0],
            template="plotly_dark",
            color_continuous_scale="rainbow"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Radar Chart":

        sample = filtered_df[numeric_cols].mean()

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=sample.values,
            theta=sample.index,
            fill='toself'
        ))

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Correlation Heatmap":

        corr = filtered_df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="inferno",
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="3D Surface":

        z = np.outer(filtered_df[numeric_cols[0]][:50], filtered_df[numeric_cols[1]][:50])

        fig = go.Figure(data=[go.Surface(z=z, colorscale='viridis')])

        fig.update_layout(template="plotly_dark")

        st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# AI INSIGHTS GENERATOR
# --------------------------------------------------

elif menu=="AI Insights":

    st.title("🤖 AI Data Insights")

    st.write("Automatic insights generated from dataset")

    for col in numeric_cols:

        st.write(f"**{col}**")

        st.write("Mean:", round(filtered_df[col].mean(),2))
        st.write("Max:", filtered_df[col].max())
        st.write("Min:", filtered_df[col].min())

# --------------------------------------------------
# AUTO ML MODEL SELECTION
# --------------------------------------------------

elif menu=="Auto ML Prediction":

    st.title("🧠 Auto Machine Learning")

    target = st.selectbox("Target Variable", numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=filtered_df[features].fillna(0)
    y=filtered_df[target].fillna(0)

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    models={
    "LinearRegression":LinearRegression(),
    "RandomForest":RandomForestRegressor(),
    "DecisionTree":DecisionTreeRegressor()
    }

    scores={}

    for name,model in models.items():

        model.fit(X_train,y_train)

        preds=model.predict(X_test)

        scores[name]=r2_score(y_test,preds)

    best=max(scores,key=scores.get)

    st.success(f"Best Model: {best}")

# --------------------------------------------------
# POWER BI
# --------------------------------------------------

elif menu=="Power BI Dashboard":

    st.title("Power BI Dashboard")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# --------------------------------------------------
# PDF REPORT
# --------------------------------------------------

elif menu=="Generate PDF Report":

    st.title("Generate Report")

    if st.button("Create PDF"):

        buffer = io.BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Intelligence Report")
        pdf.drawString(100,720,f"Rows: {filtered_df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {filtered_df.shape[1]}")

        pdf.save()

        st.download_button(
            "Download PDF",
            buffer.getvalue(),
            "report.pdf",
            "application/pdf"
        )

# --------------------------------------------------
# ABOUT
# --------------------------------------------------

elif menu=="About":

    st.write("""
Enterprise-grade **data intelligence dashboard**.

Features:

• 3D global visualization  
• animated analytics  
• AI insights  
• auto ML prediction  
• professional filters  
• Power BI integration  
• PDF analytics reports
""")
