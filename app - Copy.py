import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Global Income Distribution Dashboard", layout="wide")

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
color:#cbb6ff;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    df = pd.read_csv("final.sheet.csv")
    return df

df = load_data()

# ---------------- LOGIN ---------------- #

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='title'>Global Income Distribution Dashboard</div>",unsafe_allow_html=True)

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "admin" and pw == "1234":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# ---------------- SIDEBAR ---------------- #

menu = st.sidebar.selectbox("Navigation",[
"Dataset Overview",
"Power BI Dashboard",
"Data Explorer",
"Charts",
"Country Analysis",
"About"
])

# ---------------- DATASET OVERVIEW ---------------- #

if menu=="Dataset Overview":

    st.markdown("<div class='title'>Dataset Overview</div>",unsafe_allow_html=True)

    st.write("Dataset Preview")
    st.dataframe(df)

    st.write("Dataset Shape")
    st.write(df.shape)

    st.write("Column Names")
    st.write(list(df.columns))

# ---------------- POWER BI ---------------- #

elif menu=="Power BI Dashboard":

    st.title("Power BI Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url, height=700)

# ---------------- DATA EXPLORER ---------------- #

elif menu=="Data Explorer":

    st.title("Interactive Data Explorer")

    column = st.selectbox("Select Column", df.columns)

    st.write(df[column].describe())

# ---------------- CHARTS ---------------- #

elif menu=="Charts":

    st.title("Data Visualization")

    numeric_cols = df.select_dtypes(include=['float64','int64']).columns

    if len(numeric_cols) > 0:

        col = st.selectbox("Select Numeric Column", numeric_cols)

        fig = px.histogram(df, x=col, title=f"{col} Distribution")

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.warning("No numeric columns available for charts.")

# ---------------- COUNTRY ANALYSIS ---------------- #

elif menu=="Country Analysis":

    st.title("Country Analysis")

    possible_country_cols = [c for c in df.columns if "country" in c.lower()]

    if possible_country_cols:

        country_col = possible_country_cols[0]

        country = st.selectbox("Select Country", df[country_col].unique())

        filtered = df[df[country_col]==country]

        st.dataframe(filtered)

    else:

        st.warning("No country column detected in dataset.")

# ---------------- ABOUT ---------------- #

elif menu=="About":

    st.write("""
This dashboard analyzes the dataset **final.sheet.csv** from the GitHub repository.

Features:
- Dataset exploration
- Interactive visualizations
- Country-level analysis
- Embedded Power BI dashboard

Built using:
- Streamlit
- Plotly
- Power BI
""")
