import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from reportlab.pdfgen import canvas
import io
import random

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# ---------------- UI STYLE ---------------- #

st.markdown("""
<style>

body{
background:linear-gradient(135deg,#0e0033,#1c004d);
color:white;
}

.title{
font-size:42px;
text-align:center;
font-weight:bold;
color:#d0bfff;
}

.card{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:15px;
backdrop-filter:blur(10px);
box-shadow:0px 8px 25px rgba(0,0,0,0.6);
text-align:center;
}

.metric{
font-size:28px;
font-weight:bold;
color:#9c8cff;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ---------------- #

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='title'>Global Income Intelligence Platform</div>",unsafe_allow_html=True)

    username=st.text_input("Username")
    password=st.text_input("Password",type="password")

    if st.button("Login"):

        if username=="admin" and password=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# ---------------- SIDEBAR ---------------- #

menu=st.sidebar.selectbox("Navigation",[
"Executive Dashboard",
"Power BI Dashboard",
"World Bank Dataset",
"Global Inequality Map",
"3D Globe",
"Inequality Trends",
"Country Comparison",
"ML Prediction",
"ML Forecasting",
"Policy Simulator",
"AI Economic Assistant",
"Generate PDF Report",
"FAQ",
"About"
])

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    url="https://raw.githubusercontent.com/datasets/gini-index/master/data/gini-index.csv"
    df=pd.read_csv(url)
    return df

df=load_data()

# ---------------- EXECUTIVE DASHBOARD ---------------- #

if menu=="Executive Dashboard":

    st.markdown("<div class='title'>Global Inequality Executive Dashboard</div>",unsafe_allow_html=True)

    latest=df[df["Year"]==df["Year"].max()]

    avg_gini=round(latest["Value"].mean(),2)

    max_country=latest.sort_values("Value",ascending=False).iloc[0]["Country Name"]
    min_country=latest.sort_values("Value").iloc[0]["Country Name"]

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.markdown(f"<div class='card'>Average Gini<div class='metric'>{avg_gini}</div></div>",unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='card'>Highest Inequality<div class='metric'>{max_country}</div></div>",unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div class='card'>Lowest Inequality<div class='metric'>{min_country}</div></div>",unsafe_allow_html=True)

    with c4:
        st.markdown(f"<div class='card'>Countries<div class='metric'>{latest.shape[0]}</div></div>",unsafe_allow_html=True)

    fig=px.bar(
        latest.sort_values("Value",ascending=False).head(20),
        x="Country Name",
        y="Value",
        title="Top 20 Countries by Inequality"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- POWER BI ---------------- #

elif menu=="Power BI Dashboard":

    st.title("Power BI Embedded Dashboard")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,height=700)

# ---------------- DATASET ---------------- #

elif menu=="World Bank Dataset":

    st.title("World Bank Gini Index Dataset")

    st.dataframe(df)

# ---------------- GLOBAL MAP ---------------- #

elif menu=="Global Inequality Map":

    st.title("Global Inequality Map")

    latest=df[df["Year"]==df["Year"].max()].dropna()

    fig=px.choropleth(
        latest,
        locations="Country Code",
        color="Value",
        hover_name="Country Name",
        color_continuous_scale="Plasma"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------- 3D GLOBE ---------------- #

elif menu=="3D Globe":

    st.title("3D Global Inequality Globe")

    latest=df[df["Year"]==df["Year"].max()].dropna()

    fig=go.Figure()

    fig.add_trace(go.Scattergeo(
        locations=latest["Country Code"],
        text=latest["Country Name"],
        mode='markers',
        marker=dict(
            size=8,
            color=latest["Value"],
            colorscale="Plasma",
            colorbar_title="Gini"
        )
    ))

    fig.update_geos(projection_type="orthographic")

    st.plotly_chart(fig,use_container_width=True)

# ---------------- TRENDS ---------------- #

elif menu=="Inequality Trends":

    st.title("Inequality Trends Over Time")

    country=st.selectbox("Select Country",df["Country Name"].unique())

    cdf=df[df["Country Name"]==country]

    fig=px.line(cdf,x="Year",y="Value",title=f"{country} Inequality Trend")

    st.plotly_chart(fig,use_container_width=True)

# ---------------- COUNTRY COMPARISON ---------------- #

elif menu=="Country Comparison":

    st.title("Country Comparison")

    c1=st.selectbox("Country 1",df["Country Name"].unique())
    c2=st.selectbox("Country 2",df["Country Name"].unique())

    year=df["Year"].max()

    g1=df[(df["Country Name"]==c1)&(df["Year"]==year)]["Value"].values
    g2=df[(df["Country Name"]==c2)&(df["Year"]==year)]["Value"].values

    if len(g1)>0 and len(g2)>0:

        fig=go.Figure()

        fig.add_bar(name=c1,x=["Gini"],y=[g1[0]])
        fig.add_bar(name=c2,x=["Gini"],y=[g2[0]])

        st.plotly_chart(fig,use_container_width=True)

# ---------------- ML PREDICTION ---------------- #

elif menu=="ML Prediction":

    st.title("ML Prediction Model")

    model_df=df.dropna()

    X=model_df[["Year"]]
    y=model_df["Value"]

    model=LinearRegression()
    model.fit(X,y)

    year=st.slider("Future Year",2025,2050,2030)

    pred=model.predict([[year]])[0]

    st.metric("Predicted Global Gini Index",round(pred,2))

# ---------------- ML FORECASTING ---------------- #

elif menu=="ML Forecasting":

    st.title("Advanced ML Forecast")

    model_df=df.dropna()

    X=model_df[["Year"]]
    y=model_df["Value"]

    model=RandomForestRegressor()

    model.fit(X,y)

    year=st.slider("Forecast Year",2025,2050,2035)

    pred=model.predict([[year]])[0]

    st.metric("Forecasted Inequality",round(pred,2))

# ---------------- POLICY SIMULATOR ---------------- #

elif menu=="Policy Simulator":

    st.title("Policy Impact Simulator")

    tax=st.slider("Tax Rate",0,60,20)
    welfare=st.slider("Welfare Spending",0,50,15)

    base=45

    new_gini=base-(tax*0.2)-(welfare*0.1)

    st.metric("Estimated Gini Index",round(new_gini,2))

# ---------------- AI ASSISTANT ---------------- #

elif menu=="AI Economic Assistant":

    st.title("AI Economic Assistant")

    question=st.text_input("Ask about income inequality")

    responses=[
        "Higher education levels often reduce inequality.",
        "Strong welfare systems lower income gaps.",
        "Economic growth sometimes increases inequality initially.",
        "Progressive taxation redistributes wealth."
    ]

    if st.button("Ask AI"):
        st.success(random.choice(responses))

# ---------------- PDF REPORT ---------------- #

elif menu=="Generate PDF Report":

    st.title("Generate Inequality Report")

    if st.button("Create PDF Report"):

        buffer=io.BytesIO()

        pdf=canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Inequality Report")
        pdf.drawString(100,720,"Generated by Global Income Intelligence Platform")

        pdf.save()

        st.download_button(
            "Download Report",
            buffer.getvalue(),
            "inequality_report.pdf",
            "application/pdf"
        )

# ---------------- FAQ ---------------- #

elif menu=="FAQ":

    with st.expander("What is Gini Index?"):
        st.write("The Gini Index measures income inequality from 0 (perfect equality) to 100 (perfect inequality).")

    with st.expander("Why does inequality matter?"):
        st.write("High inequality can affect economic growth and social stability.")

# ---------------- ABOUT ---------------- #

elif menu=="About":

    st.write("""
Global Income Intelligence Platform

Technologies Used:
• Streamlit  
• Plotly  
• Power BI  
• Machine Learning  

Dataset Source:
World Bank Gini Index
""")
