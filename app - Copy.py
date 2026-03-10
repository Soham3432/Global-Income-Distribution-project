import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

st.set_page_config(layout="wide", page_title="Analytics SaaS Platform")

# ---------------------------------------------------
# DARK SaaS UI
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#020617,#020617,#0f172a,#020617);
color:white;
font-family:Segoe UI;
}

/* TOP BAR */

.topbar{
display:flex;
justify-content:space-between;
align-items:center;
padding:12px 20px;
background:#020617;
border-bottom:1px solid #1e293b;
}

.logo{
font-size:22px;
font-weight:700;
background:linear-gradient(90deg,#3b82f6,#22c55e,#ec4899);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

/* SIDEBAR TREE */

.sidebar-tree{
padding:10px;
border-right:1px solid #1e293b;
height:100vh;
}

/* WORKSPACE PANEL */

.workspace{
padding:20px;
}

/* CARD */

.card{
background:#020617;
padding:15px;
border-radius:10px;
border:1px solid #1e293b;
text-align:center;
}

/* BUTTONS */

.stButton>button{
background:#1e293b;
color:white;
border-radius:6px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TOP TOOLBAR
# ---------------------------------------------------

st.markdown("""
<div class="topbar">
<div class="logo">Analytics Studio</div>
<div>AI Data Platform</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

sidebar, main, ai_panel = st.columns([1.3,4,1.5])

# ---------------------------------------------------
# DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

if "data" not in st.session_state:
    st.session_state.data = load_data()

df = st.session_state.data

numeric = df.select_dtypes(include=["int64","float64"]).columns
categorical = df.select_dtypes(include=["object"]).columns

# ---------------------------------------------------
# PROJECT FILE TREE SIDEBAR
# ---------------------------------------------------

with sidebar:

    st.markdown("### Project Explorer")

    page = st.radio(
        "",
        [
            "Dashboard",
            "Charts",
            "Statistics",
            "Machine Learning",
            "Forecasting",
            "Power BI",
            "Dataset",
            "Reports"
        ]
    )

# ---------------------------------------------------
# MAIN WORKSPACE WITH TABS
# ---------------------------------------------------

with main:

    st.markdown("## Workspace")

    tabs = st.tabs(["Dashboard","Charts","ML","Insights"])

# ---------------------------------------------------
# DASHBOARD TAB
# ---------------------------------------------------

    with tabs[0]:

        st.subheader("Executive Dashboard")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Rows", df.shape[0])
        c2.metric("Columns", df.shape[1])
        c3.metric("Numeric", len(numeric))
        c4.metric("Categorical", len(categorical))

        if len(numeric)>0:

            fig, ax = plt.subplots(figsize=(3,2))

            ax.hist(df[numeric[0]], color="#3b82f6")

            st.pyplot(fig)

# ---------------------------------------------------
# CHART TAB
# ---------------------------------------------------

    with tabs[1]:

        st.subheader("Chart Explorer")

        chart = st.selectbox(
            "Chart Type",
            ["Bar","Line","Scatter","Pie"]
        )

        if chart == "Bar":

            col = st.selectbox("Column", numeric)

            fig, ax = plt.subplots(figsize=(3,2))
            ax.bar(range(len(df[col])), df[col], color="#22c55e")
            st.pyplot(fig)

        if chart == "Line":

            col = st.selectbox("Column", numeric)

            fig, ax = plt.subplots(figsize=(3,2))
            ax.plot(df[col], color="#ec4899")
            st.pyplot(fig)

        if chart == "Scatter":

            x = st.selectbox("X", numeric)
            y = st.selectbox("Y", numeric)

            fig, ax = plt.subplots(figsize=(3,2))
            ax.scatter(df[x], df[y], color="#3b82f6")
            st.pyplot(fig)

        if chart == "Pie":

            col = st.selectbox("Category", categorical)

            data = df[col].value_counts()

            fig, ax = plt.subplots(figsize=(3,2))
            ax.pie(data.values, labels=data.index)
            st.pyplot(fig)

# ---------------------------------------------------
# MACHINE LEARNING TAB
# ---------------------------------------------------

    with tabs[2]:

        st.subheader("Prediction Model")

        target = st.selectbox("Target Column", numeric)

        features = [c for c in numeric if c != target]

        X = df[features]
        y = df[target]

        model = RandomForestRegressor()

        model.fit(X,y)

        inputs = []

        for f in features:

            val = st.number_input(f, value=float(X[f].mean()))

            inputs.append(val)

        if st.button("Predict"):

            pred = model.predict([inputs])[0]

            st.success(f"Prediction: {pred}")

            st.write("Model R2:", r2_score(y, model.predict(X)))

# ---------------------------------------------------
# INSIGHTS TAB
# ---------------------------------------------------

    with tabs[3]:

        st.subheader("AI Data Insights")

        st.write("Dataset shape:", df.shape)

        st.write("Missing Values")

        st.write(df.isnull().sum())

        st.write("Correlation Matrix")

        st.write(df.corr(numeric_only=True))

# ---------------------------------------------------
# SPLIT SCREEN POWER BI
# ---------------------------------------------------

    st.subheader("Split Screen Analytics")

    left,right = st.columns(2)

    with left:

        st.write("Python Charts")

        if len(numeric)>0:

            fig, ax = plt.subplots(figsize=(3,2))
            ax.hist(df[numeric[0]], color="#3b82f6")
            st.pyplot(fig)

    with right:

        st.write("Power BI Dashboard")

        st.components.v1.iframe(
        "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9",
        height=420
        )

# ---------------------------------------------------
# AI ASSISTANT PANEL
# ---------------------------------------------------

with ai_panel:

    st.markdown("### AI Assistant")

    question = st.text_input("Ask about your dataset")

    if question:

        st.write("AI Insight:")

        st.write(
        "Based on the dataset structure, numeric variables appear to dominate. Consider correlation analysis and forecasting for deeper insights."
        )
