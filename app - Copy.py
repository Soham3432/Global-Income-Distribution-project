import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Income Distribution Platform", layout="wide")

# ---------------- STYLE ---------------- #

st.markdown("""
<style>
body{
background:linear-gradient(135deg,#0e0033,#1c004d);
color:white;
}
.title{
font-size:40px;
font-weight:bold;
text-align:center;
color:#d0bfff;
}
.card{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:12px;
text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    df = pd.read_csv("final.sheet.csv")
    return df

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# ---------------- LOGIN ---------------- #

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='title'>Global Income Distribution Dashboard</div>",unsafe_allow_html=True)

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# ---------------- SIDEBAR ---------------- #

menu = st.sidebar.selectbox("Navigation",[
"Executive Dashboard",
"Power BI Dashboard",
"Dataset Explorer",
"Interactive Charts",
"Country Analysis",
"Machine Learning Prediction",
"ML Forecasting",
"Generate PDF Report",
"About"
])

# ---------------- EXECUTIVE DASHBOARD ---------------- #

if menu=="Executive Dashboard":

    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)

    st.write("Dataset Shape:", df.shape)

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("Rows", df.shape[0])

    with col2:
        st.metric("Columns", df.shape[1])

    with col3:
        st.metric("Numeric Variables", len(numeric_cols))

    if len(numeric_cols)>0:

        fig = px.histogram(df, x=numeric_cols[0], title=f"{numeric_cols[0]} Distribution")

        st.plotly_chart(fig,use_container_width=True)

# ---------------- POWER BI ---------------- #

elif menu=="Power BI Dashboard":

    st.title("Power BI Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# ---------------- DATA EXPLORER ---------------- #

elif menu=="Dataset Explorer":

    st.title("Dataset Explorer")

    st.dataframe(df)

    column = st.selectbox("Select Column", df.columns)

    st.write(df[column].describe())

# ---------------- INTERACTIVE CHARTS ---------------- #

elif menu=="Interactive Charts":

    st.title("Interactive Visualizations")

    if len(numeric_cols)>0:

        x = st.selectbox("X Axis", numeric_cols)
        y = st.selectbox("Y Axis", numeric_cols)

        fig = px.scatter(df, x=x, y=y)

        st.plotly_chart(fig,use_container_width=True)

# ---------------- COUNTRY ANALYSIS ---------------- #

elif menu=="Country Analysis":

    st.title("Country Analysis")

    country_cols = [c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col = country_cols[0]

        country = st.selectbox("Select Country", df[country_col].unique())

        filtered = df[df[country_col]==country]

        st.dataframe(filtered)

        if len(numeric_cols)>0:

            fig = px.bar(filtered, y=numeric_cols[0])

            st.plotly_chart(fig,use_container_width=True)

    else:

        st.warning("No country column detected.")

# ---------------- ML PREDICTION ---------------- #

elif menu=="Machine Learning Prediction":

    st.title("Machine Learning Prediction")

    if len(numeric_cols)>=2:

        target = st.selectbox("Select Target Variable", numeric_cols)

        features = [c for c in numeric_cols if c!=target]

        X = df[features].fillna(0)
        y = df[target].fillna(0)

        model = LinearRegression()

        model.fit(X,y)

        inputs=[]

        st.write("Enter feature values")

        for col in features:

            val = st.number_input(col,value=float(X[col].mean()))

            inputs.append(val)

        prediction = model.predict([inputs])[0]

        st.success(f"Predicted {target}: {prediction}")

    else:

        st.warning("Not enough numeric columns for ML.")

# ---------------- ML FORECASTING ---------------- #

elif menu=="ML Forecasting":

    st.title("Advanced ML Forecast")

    if len(numeric_cols)>=2:

        target = st.selectbox("Target Variable", numeric_cols)

        features = [c for c in numeric_cols if c!=target]

        X = df[features].fillna(0)
        y = df[target].fillna(0)

        model = RandomForestRegressor()

        model.fit(X,y)

        inputs=[]

        for col in features:

            val = st.number_input(col,value=float(X[col].mean()))

            inputs.append(val)

        prediction = model.predict([inputs])[0]

        st.success(f"Forecasted {target}: {prediction}")

# ---------------- PDF REPORT ---------------- #

elif menu=="Generate PDF Report":

    st.title("Generate Report")

    if st.button("Create PDF"):

        buffer = io.BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Distribution Report")
        pdf.drawString(100,720,f"Dataset rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Dataset columns: {df.shape[1]}")

        pdf.save()

        st.download_button(
            "Download PDF",
            buffer.getvalue(),
            "report.pdf",
            "application/pdf"
        )

# ---------------- ABOUT ---------------- #

elif menu=="About":

    st.write("""
This dashboard analyzes the dataset **final.sheet.csv** from the GitHub repository.

Features included:
- Interactive Plotly visualizations
- Machine Learning prediction models
- Random Forest forecasting
- Embedded Power BI dashboard
- PDF report generation

Built with:
- Streamlit
- Plotly
- Scikit-learn
- ReportLab
""")
