import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io

st.set_page_config(layout="wide", page_title="Analytics Studio")

# -------------------------------------------------
# OVERLEAF STYLE UI
# -------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#f6f8fb;
}

/* Top toolbar */

.toolbar{
display:flex;
justify-content:space-between;
align-items:center;
padding:10px 20px;
background:white;
border-bottom:1px solid #e5e7eb;
}

.logo{
font-size:22px;
font-weight:bold;
color:#2563eb;
}

/* Sidebar */

.sidebar{
background:white;
border-right:1px solid #e5e7eb;
padding:20px;
height:100vh;
}

/* Cards */

.card{
background:white;
padding:15px;
border-radius:10px;
box-shadow:0 2px 10px rgba(0,0,0,0.08);
text-align:center;
}

/* Buttons */

.stButton>button{
background:#2563eb;
color:white;
border-radius:6px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TOP TOOLBAR
# -------------------------------------------------

st.markdown("""
<div class="toolbar">
<div class="logo">Analytics Studio</div>
<div>Data Science Dashboard Workspace</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LAYOUT
# -------------------------------------------------

sidebar, main = st.columns([1,4])

# -------------------------------------------------
# DATA
# -------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

if "data" not in st.session_state:
    st.session_state.data = load_data()

df = st.session_state.data

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# -------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------

with sidebar:

    st.markdown("### Workspace Menu")

    page = st.radio(
        "",
        [
            "Dashboard",
            "Power BI Dashboard",
            "Upload Dataset",
            "Chart Explorer",
            "Chart Explainer",
            "Statistics Lab",
            "AI Insights",
            "Correlation Analyzer",
            "Forecasting",
            "Machine Learning",
            "Report Generator",
            "FAQ"
        ]
    )

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

with main:

    if page == "Dashboard":

        st.title("Executive Analytics Dashboard")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Rows", df.shape[0])
        c2.metric("Columns", df.shape[1])
        c3.metric("Numeric Features", len(numeric_cols))
        c4.metric("Categorical Features", len(categorical_cols))

        if len(numeric_cols) > 0:

            fig, ax = plt.subplots(figsize=(3,2))
            ax.hist(df[numeric_cols[0]], color="blue")
            st.pyplot(fig)

# -------------------------------------------------
# POWER BI EMBED
# -------------------------------------------------

    elif page == "Power BI Dashboard":

        st.title("Power BI Dashboard")

        st.components.v1.iframe(
            "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9",
            height=650
        )

# -------------------------------------------------
# DATASET UPLOAD
# -------------------------------------------------

    elif page == "Upload Dataset":

        st.title("Upload Dataset")

        file = st.file_uploader("Upload CSV")

        if file:

            st.session_state.data = pd.read_csv(file)

            st.success("Dataset Uploaded")

            st.dataframe(st.session_state.data.head())

# -------------------------------------------------
# CHART EXPLORER
# -------------------------------------------------

    elif page == "Chart Explorer":

        st.title("Chart Explorer")

        chart = st.selectbox(
            "Chart Type",
            ["Bar","Line","Scatter","Pie"]
        )

        if chart == "Bar":

            col = st.selectbox("Column", numeric_cols)

            fig, ax = plt.subplots(figsize=(3,2))
            ax.bar(range(len(df[col])), df[col], color="green")
            st.pyplot(fig)

        elif chart == "Line":

            col = st.selectbox("Column", numeric_cols)

            fig, ax = plt.subplots(figsize=(3,2))
            ax.plot(df[col], color="red")
            st.pyplot(fig)

        elif chart == "Scatter":

            x = st.selectbox("X", numeric_cols)
            y = st.selectbox("Y", numeric_cols)

            fig, ax = plt.subplots(figsize=(3,2))
            ax.scatter(df[x], df[y], color="blue")
            st.pyplot(fig)

        elif chart == "Pie":

            col = st.selectbox("Category", categorical_cols)

            data = df[col].value_counts()

            fig, ax = plt.subplots(figsize=(3,2))
            ax.pie(data.values, labels=data.index)
            st.pyplot(fig)

# -------------------------------------------------
# CHART EXPLAINER
# -------------------------------------------------

    elif page == "Chart Explainer":

        st.title("Chart Explainer")

        explain = {

        "Bar Chart":"Used to compare categories such as sales by region.",

        "Line Chart":"Used for time trend analysis such as revenue growth.",

        "Scatter Plot":"Used to identify correlations between variables.",

        "Pie Chart":"Used to display percentage distribution."
        }

        c = st.selectbox("Chart", list(explain.keys()))

        st.write(explain[c])

# -------------------------------------------------
# STATISTICS LAB
# -------------------------------------------------

    elif page == "Statistics Lab":

        st.title("Statistical Analysis")

        col = st.selectbox("Column", numeric_cols)

        st.write(df[col].describe())

        fig, ax = plt.subplots(figsize=(3,2))
        ax.boxplot(df[col])
        st.pyplot(fig)

# -------------------------------------------------
# AI INSIGHTS
# -------------------------------------------------

    elif page == "AI Insights":

        st.title("Automated Insights")

        st.write("Dataset Shape:", df.shape)

        st.write("Missing Values")

        st.write(df.isnull().sum())

        st.write("Correlation")

        st.write(df.corr(numeric_only=True))

# -------------------------------------------------
# CORRELATION
# -------------------------------------------------

    elif page == "Correlation Analyzer":

        st.title("Correlation Heatmap")

        corr = df.corr(numeric_only=True)

        fig, ax = plt.subplots(figsize=(3,2))

        cax = ax.imshow(corr)

        fig.colorbar(cax)

        st.pyplot(fig)

# -------------------------------------------------
# FORECASTING
# -------------------------------------------------

    elif page == "Forecasting":

        st.title("Time Series Forecasting")

        col = st.selectbox("Target", numeric_cols)

        df["t"] = range(len(df))

        X = df[["t"]]

        y = df[col]

        model = LinearRegression()

        model.fit(X,y)

        future = st.slider("Future",1,30,10)

        future_x = np.arange(len(df), len(df)+future).reshape(-1,1)

        pred = model.predict(future_x)

        fig, ax = plt.subplots(figsize=(3,2))

        ax.plot(df[col])
        ax.plot(range(len(df), len(df)+future), pred)

        st.pyplot(fig)

# -------------------------------------------------
# MACHINE LEARNING
# -------------------------------------------------

    elif page == "Machine Learning":

        st.title("Prediction Model")

        target = st.selectbox("Target", numeric_cols)

        features = [c for c in numeric_cols if c != target]

        X = df[features]

        y = df[target]

        model = RandomForestRegressor()

        model.fit(X,y)

        inputs=[]

        for f in features:

            val = st.number_input(f, value=float(X[f].mean()))

            inputs.append(val)

        if st.button("Predict"):

            p = model.predict([inputs])[0]

            st.success(f"Prediction: {p}")

            st.write("Model R2:", r2_score(y, model.predict(X)))

# -------------------------------------------------
# PDF REPORT
# -------------------------------------------------

    elif page == "Report Generator":

        st.title("PDF Report")

        if st.button("Generate Report"):

            buffer = io.BytesIO()

            pdf = canvas.Canvas(buffer)

            pdf.drawString(100,750,"Analytics Report")

            pdf.drawString(100,720,f"Rows: {df.shape[0]}")

            pdf.drawString(100,700,f"Columns: {df.shape[1]}")

            pdf.save()

            st.download_button(
                "Download",
                buffer.getvalue(),
                "report.pdf"
            )

# -------------------------------------------------
# FAQ
# -------------------------------------------------

    elif page == "FAQ":

        st.title("FAQ")

        faq = {

        "Why combine Power BI with Python?":
        "To combine enterprise dashboards with advanced analytics.",

        "Why forecasting is useful?":
        "It predicts future trends using historical data.",

        "Why correlation analysis matters?":
        "It identifies relationships between variables."

        }

        q = st.selectbox("Question", list(faq.keys()))

        st.write(faq[q])
