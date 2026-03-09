import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import time

st.set_page_config(page_title="AI Data Intelligence Platform", layout="wide")

# ------------------------------------------------
# ULTRA MODERN UI
# ------------------------------------------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#0f172a,#020617);
color:white;
font-family:Inter;
}

.big-title{
font-size:52px;
font-weight:900;
text-align:center;
background:linear-gradient(90deg,#22c1c3,#fdbb2d);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.card{
background:rgba(255,255,255,0.04);
border-radius:20px;
padding:20px;
backdrop-filter:blur(20px);
box-shadow:0 20px 60px rgba(0,0,0,0.6);
}

.stButton>button{
background:linear-gradient(90deg,#00c6ff,#0072ff);
border:none;
border-radius:12px;
color:white;
padding:8px 20px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns

# ------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------

menu = st.sidebar.selectbox("Navigation",[
"Live Streaming Dashboard",
"3D Rotating Globe",
"AI Forecast Engine",
"Automatic Insights",
"AI Data Analyst",
"About"
])

# ------------------------------------------------
# LIVE STREAMING CHART
# ------------------------------------------------

if menu=="Live Streaming Dashboard":

    st.markdown("<div class='big-title'>⚡ Real-Time Data Stream</div>",unsafe_allow_html=True)

    chart_placeholder = st.empty()

    data = []

    for i in range(50):

        data.append(np.random.randn())

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            y=data,
            mode='lines',
            line=dict(color='#22c1c3',width=3)
        ))

        fig.update_layout(
        template="plotly_dark",
        title="Live KPI Streaming",
        )

        chart_placeholder.plotly_chart(fig,use_container_width=True)

        time.sleep(0.3)

# ------------------------------------------------
# 3D ROTATING GLOBE
# ------------------------------------------------

elif menu=="3D Rotating Globe":

    st.markdown("<div class='big-title'>🌍 Global Data Globe</div>",unsafe_allow_html=True)

    if "country" in [c.lower() for c in df.columns]:

        country_col=[c for c in df.columns if "country" in c.lower()][0]

        fig = px.scatter_geo(
            df,
            locations=country_col,
            locationmode="country names",
            size=numeric_cols[0],
            color=numeric_cols[0],
            projection="orthographic"
        )

        fig.update_layout(
        template="plotly_dark",
        title="3D Rotating World Map"
        )

        st.plotly_chart(fig,use_container_width=True)

    else:

        st.warning("No country column detected.")

# ------------------------------------------------
# AI FORECAST ENGINE
# ------------------------------------------------

elif menu=="AI Forecast Engine":

    st.markdown("<div class='big-title'>📈 AI Forecast Engine</div>",unsafe_allow_html=True)

    target = st.selectbox("Select Prediction Target", numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    model=RandomForestRegressor()

    model.fit(X_train,y_train)

    preds=model.predict(X_test)

    fig=go.Figure()

    fig.add_trace(go.Scatter(y=y_test,mode="lines",name="Actual"))
    fig.add_trace(go.Scatter(y=preds,mode="lines",name="Predicted"))

    fig.update_layout(
    template="plotly_dark",
    title="Forecast Prediction Graph"
    )

    st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# AUTO INSIGHTS
# ------------------------------------------------

elif menu=="Automatic Insights":

    st.markdown("<div class='big-title'>🧠 Automatic Insight Story</div>",unsafe_allow_html=True)

    for col in numeric_cols:

        mean=df[col].mean()
        maxv=df[col].max()
        minv=df[col].min()

        st.markdown(f"""
        **Insight for {col}**

        • Average value is **{round(mean,2)}**  
        • Maximum recorded value is **{maxv}**  
        • Minimum recorded value is **{minv}**

        """)

# ------------------------------------------------
# AI DATA ANALYST
# ------------------------------------------------

elif menu=="AI Data Analyst":

    st.markdown("<div class='big-title'>🤖 AI Data Analyst</div>",unsafe_allow_html=True)

    question = st.text_input("Ask a question about the dataset")

    if question:

        st.write("Dataset Shape:", df.shape)

        for col in numeric_cols[:3]:

            st.write(f"{col} average:",round(df[col].mean(),2))

        st.info("AI suggestion: explore correlations between variables.")

# ------------------------------------------------
# ABOUT
# ------------------------------------------------

elif menu=="About":

    st.markdown("<div class='big-title'>AI Data Platform</div>",unsafe_allow_html=True)

    st.write("""
This project demonstrates a **modern AI-driven analytics dashboard**.

Capabilities:

• Real-time streaming analytics  
• 3D global visualization  
• AI forecasting models  
• automatic insight storytelling  
• AI data assistant  

Built with Streamlit + Plotly + Machine Learning.
""")
