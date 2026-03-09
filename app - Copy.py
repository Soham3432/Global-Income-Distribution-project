import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="Global Income Distribution AI Analytics",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------
# GLASSMORPHISM UI
# -------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(120deg,#0f2027,#203a43,#2c5364);
    color:white;
}

.block-container{
    padding-top:2rem;
}

.card{
    background:rgba(255,255,255,0.1);
    padding:20px;
    border-radius:15px;
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# DATA LOAD
# -------------------------------

@st.cache_data
def load_data():

    try:
        df = pd.read_csv("final.sheet.csv")
    except:
        st.error("Dataset final.sheet.csv not found")
        st.stop()

    df.columns = [c.strip() for c in df.columns]

    return df


df = load_data()

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("⚙️ Controls")

year_col = None
country_col = None
value_col = None

for c in df.columns:
    if "year" in c.lower():
        year_col = c
    if "country" in c.lower():
        country_col = c
    if "value" in c.lower():
        value_col = c

if year_col is None:
    year_col = df.columns[0]

if country_col is None:
    country_col = df.columns[1]

if value_col is None:
    value_col = df.columns[-1]

years = sorted(df[year_col].dropna().unique())

selected_year = st.sidebar.selectbox("Select Year", years)

countries = sorted(df[country_col].dropna().unique())

selected_country = st.sidebar.selectbox("Country", countries)

# -------------------------------
# HEADER
# -------------------------------

st.title("🌍 Global Income Distribution AI Analytics Platform")

st.markdown("Advanced analytics dashboard using your dataset.")

# -------------------------------
# FILTER DATA
# -------------------------------

year_data = df[df[year_col] == selected_year]

country_data = df[df[country_col] == selected_country]

# -------------------------------
# KPI SECTION
# -------------------------------

col1,col2,col3 = st.columns(3)

try:
    avg_income = year_data[value_col].mean()
except:
    avg_income = 0

try:
    max_country = year_data.sort_values(value_col,ascending=False).iloc[0][country_col]
except:
    max_country = "N/A"

try:
    min_country = year_data.sort_values(value_col).iloc[0][country_col]
except:
    min_country = "N/A"

col1.metric("Average Value", round(avg_income,2))
col2.metric("Top Country", max_country)
col3.metric("Lowest Country", min_country)

# -------------------------------
# GLOBAL MAP
# -------------------------------

st.subheader("🌎 Global Distribution Map")

try:

    fig = px.choropleth(
        year_data,
        locations=country_col,
        locationmode="country names",
        color=value_col,
        title="Global Income Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

except:
    st.info("Map cannot be generated with current dataset format")

# -------------------------------
# TREND CHART
# -------------------------------

st.subheader("📈 Country Trend")

try:

    fig2 = px.line(
        country_data,
        x=year_col,
        y=value_col,
        title=f"{selected_country} Trend"
    )

    st.plotly_chart(fig2, use_container_width=True)

except:
    st.info("Trend chart unavailable")

# -------------------------------
# TOP COUNTRIES
# -------------------------------

st.subheader("🏆 Top Countries")

try:

    top10 = year_data.sort_values(value_col,ascending=False).head(10)

    fig3 = px.bar(
        top10,
        x=country_col,
        y=value_col,
        title="Top 10 Countries"
    )

    st.plotly_chart(fig3, use_container_width=True)

except:
    st.info("Top countries chart unavailable")

# -------------------------------
# ML INEQUALITY PREDICTION
# -------------------------------

st.subheader("🧠 ML Forecast")

try:

    temp = country_data[[year_col,value_col]].dropna()

    X = temp[[year_col]]
    y = temp[value_col]

    model = LinearRegression()
    model.fit(X,y)

    future_year = st.slider("Predict Future Year", int(min(years)), int(max(years)+20))

    prediction = model.predict([[future_year]])[0]

    st.success(f"Predicted value for {selected_country} in {future_year}: {round(prediction,2)}")

except:
    st.info("Prediction unavailable")

# -------------------------------
# 3D GLOBE (SIMULATED)
# -------------------------------

st.subheader("🌍 3D Global Scatter")

try:

    fig4 = px.scatter_geo(
        year_data,
        locations=country_col,
        locationmode="country names",
        size=value_col,
        projection="orthographic"
    )

    st.plotly_chart(fig4, use_container_width=True)

except:
    st.info("3D globe unavailable")

# -------------------------------
# POWER BI EMBED
# -------------------------------

st.subheader("📊 Power BI Dashboard")

power_bi_url = st.text_input(
    "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9" 
)

if power_bi_url:

    st.components.v1.iframe(
        power_bi_url,
        height=600
    )

# -------------------------------
# AI INSIGHTS
# -------------------------------

st.subheader("🤖 AI Insights")

try:

    insight1 = f"Average value in {selected_year} is {round(avg_income,2)}."

    insight2 = f"{max_country} leads the dataset."

    insight3 = f"{min_country} shows lowest value."

    st.write("•", insight1)
    st.write("•", insight2)
    st.write("•", insight3)

except:
    st.write("Insights unavailable")

# -------------------------------
# SIMPLE CHAT ASSISTANT
# -------------------------------

st.subheader("💬 Analytics Assistant")

user_question = st.text_input("Ask about the dataset")

if user_question:

    if "average" in user_question.lower():
        st.write(f"Average value is {round(avg_income,2)}")

    elif "top" in user_question.lower():
        st.write(f"Top country is {max_country}")

    else:
        st.write("Try asking about average or top country.")

# -------------------------------
# PDF REPORT
# -------------------------------

st.subheader("📄 Generate Report")

if st.button("Generate PDF"):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("Global Income Distribution Report", styles["Title"]))

    story.append(Spacer(1,20))

    story.append(Paragraph(f"Year: {selected_year}", styles["Normal"]))
    story.append(Paragraph(f"Average Value: {round(avg_income,2)}", styles["Normal"]))
    story.append(Paragraph(f"Top Country: {max_country}", styles["Normal"]))

    doc.build(story)

    st.download_button(
        "Download PDF",
        buffer.getvalue(),
        file_name="report.pdf"
    )
