import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# ---------------- ADVANCED 3D UI STYLE ---------------- #

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background */

.stApp{
background: linear-gradient(135deg,#09001f,#14003d,#24005f);
color:white;
}

/* Title */

.main-title{
font-size:48px;
font-weight:700;
text-align:center;
background: linear-gradient(90deg,#a855f7,#6366f1);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:20px;
}

/* Glass Cards */

.card{
background: rgba(255,255,255,0.05);
backdrop-filter: blur(15px);
border-radius:18px;
padding:25px;
box-shadow: 0 10px 40px rgba(0,0,0,0.6);
transition:0.4s;
}

.card:hover{
transform: translateY(-8px) scale(1.02);
box-shadow:0 20px 60px rgba(120,0,255,0.6);
}

/* Metrics */

.metric-card{
background:linear-gradient(145deg,#2b0a68,#1a0440);
border-radius:16px;
padding:25px;
text-align:center;
box-shadow:0 10px 40px rgba(0,0,0,0.7);
}

/* Buttons */

.stButton>button{
background:linear-gradient(90deg,#7c3aed,#6366f1);
border:none;
border-radius:12px;
padding:10px 30px;
color:white;
font-weight:bold;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.05);
box-shadow:0 0 20px #7c3aed;
}

/* Sidebar */

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#0d0028,#14003d);
border-right:1px solid rgba(255,255,255,0.1);
}

/* Filter container */

.filter-box{
background:rgba(255,255,255,0.06);
padding:15px;
border-radius:15px;
box-shadow:0 10px 30px rgba(0,0,0,0.5);
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns


# ---------------- LOGIN ---------------- #

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='main-title'>🌍 Global Income Intelligence</div>", unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        user = st.text_input("👤 Username")
        pw = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Login"):
            if user=="admin" and pw=="1234":
                st.session_state.login=True
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.markdown("</div>",unsafe_allow_html=True)

    st.stop()

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🚀 Navigation")

menu = st.sidebar.radio(
"",
[
"📊 Executive Dashboard",
"📈 Power BI Dashboard",
"🔎 Dataset Explorer",
"📉 Interactive Charts",
"🌎 Country Analysis",
"🤖 ML Prediction",
"🧠 ML Forecast",
"📄 Generate Report",
"ℹ️ About"
]
)

# ---------------- EXECUTIVE DASHBOARD ---------------- #

if menu=="📊 Executive Dashboard":

    st.markdown("<div class='main-title'>Executive Analytics Dashboard</div>",unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Rows</h3>
        <h1>{df.shape[0]}</h1>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Columns</h3>
        <h1>{df.shape[1]}</h1>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <h3>Numeric Variables</h3>
        <h1>{len(numeric_cols)}</h1>
        </div>
        """,unsafe_allow_html=True)

    if len(numeric_cols)>0:

        fig = px.histogram(
            df,
            x=numeric_cols[0],
            color_discrete_sequence=["#8b5cf6"]
        )

        st.plotly_chart(fig,use_container_width=True)

# ---------------- POWER BI ---------------- #

elif menu=="📈 Power BI Dashboard":

    st.markdown("<div class='main-title'>Power BI Embedded Dashboard</div>",unsafe_allow_html=True)

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# ---------------- DATA EXPLORER ---------------- #

elif menu=="🔎 Dataset Explorer":

    st.markdown("<div class='main-title'>Dataset Explorer</div>",unsafe_allow_html=True)

    st.dataframe(df,use_container_width=True)

    st.markdown("<div class='filter-box'>",unsafe_allow_html=True)

    column = st.selectbox("Select Column", df.columns)

    st.write(df[column].describe())

    st.markdown("</div>",unsafe_allow_html=True)

# ---------------- INTERACTIVE CHARTS ---------------- #

elif menu=="📉 Interactive Charts":

    st.markdown("<div class='main-title'>Interactive Visualizations</div>",unsafe_allow_html=True)

    st.markdown("<div class='filter-box'>",unsafe_allow_html=True)

    x = st.selectbox("X Axis", numeric_cols)
    y = st.selectbox("Y Axis", numeric_cols)

    st.markdown("</div>",unsafe_allow_html=True)

    fig = px.scatter(
        df,
        x=x,
        y=y,
        color_discrete_sequence=["#a855f7"]
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- COUNTRY ANALYSIS ---------------- #

elif menu=="🌎 Country Analysis":

    st.markdown("<div class='main-title'>Country Level Analysis</div>",unsafe_allow_html=True)

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        country = st.selectbox("Select Country", df[country_col].unique())

        filtered = df[df[country_col]==country]

        st.dataframe(filtered)

        fig = px.bar(filtered,y=numeric_cols[0],color_discrete_sequence=["#6366f1"])

        st.plotly_chart(fig,use_container_width=True)

# ---------------- ML PREDICTION ---------------- #

elif menu=="🤖 ML Prediction":

    st.markdown("<div class='main-title'>Machine Learning Prediction</div>",unsafe_allow_html=True)

    target = st.selectbox("Target Variable", numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    model=LinearRegression()
    model.fit(X,y)

    inputs=[]

    st.subheader("Enter Feature Values")

    for col in features:
        val = st.number_input(col,value=float(X[col].mean()))
        inputs.append(val)

    if st.button("Predict"):

        prediction=model.predict([inputs])[0]

        st.success(f"Predicted {target}: {prediction}")

# ---------------- ML FORECAST ---------------- #

elif menu=="🧠 ML Forecast":

    st.markdown("<div class='main-title'>AI Forecasting Engine</div>",unsafe_allow_html=True)

    target = st.selectbox("Target Variable", numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    model=RandomForestRegressor()
    model.fit(X,y)

    inputs=[]

    for col in features:
        val = st.number_input(col,value=float(X[col].mean()))
        inputs.append(val)

    if st.button("Forecast"):

        prediction=model.predict([inputs])[0]

        st.success(f"Forecasted {target}: {prediction}")

# ---------------- REPORT ---------------- #

elif menu=="📄 Generate Report":

    st.markdown("<div class='main-title'>Generate Analytics Report</div>",unsafe_allow_html=True)

    if st.button("Generate PDF"):

        buffer = io.BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button("Download PDF",buffer.getvalue(),"report.pdf")

# ---------------- ABOUT ---------------- #

elif menu=="ℹ️ About":

    st.markdown("<div class='main-title'>About Platform</div>",unsafe_allow_html=True)

    st.write("""
    This platform provides **advanced analytics for global income distribution.**

    Features include:
    - Interactive dashboards
    - Embedded Power BI reports
    - Machine learning prediction
    - AI forecasting
    - PDF analytics reports
    """)
