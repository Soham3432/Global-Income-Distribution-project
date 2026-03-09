import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Global Income Distribution AI Platform",
    layout="wide",
    page_icon="🌍"
)

# ---------------------------------------------------
# GLASSMORPHISM UI
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

.card{
background:rgba(255,255,255,0.08);
padding:20px;
border-radius:15px;
backdrop-filter:blur(10px);
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("final.sheet.csv")
    except:
        st.error("❌ final.sheet.csv not found in project folder")
        st.stop()

    df.columns = [c.strip() for c in df.columns]
    return df

df = load_data()

# ---------------------------------------------------
# DETECT IMPORTANT COLUMNS
# ---------------------------------------------------

year_col=None
country_col=None
value_col=None

for col in df.columns:

    if "year" in col.lower():
        year_col=col

    if "country" in col.lower():
        country_col=col

    if "value" in col.lower():
        value_col=col

if year_col is None:
    year_col=df.columns[0]

if country_col is None:
    country_col=df.columns[1]

if value_col is None:
    value_col=df.columns[-1]

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("Dashboard Controls")

years=sorted(df[year_col].dropna().unique())
countries=sorted(df[country_col].dropna().unique())

selected_year=st.sidebar.selectbox("Select Year",years)
selected_country=st.sidebar.selectbox("Select Country",countries)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🌍 Global Income Distribution AI Dashboard")

st.write("Interactive analytics platform built using your dataset.")

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

year_data=df[df[year_col]==selected_year]
country_data=df[df[country_col]==selected_country]

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

col1,col2,col3=st.columns(3)

try:
    avg_value=year_data[value_col].mean()
except:
    avg_value=0

try:
    top_country=year_data.sort_values(value_col,ascending=False).iloc[0][country_col]
except:
    top_country="N/A"

try:
    low_country=year_data.sort_values(value_col).iloc[0][country_col]
except:
    low_country="N/A"

col1.metric("Average Value",round(avg_value,2))
col2.metric("Top Country",top_country)
col3.metric("Lowest Country",low_country)

# ---------------------------------------------------
# GLOBAL MAP
# ---------------------------------------------------

st.subheader("🌎 Global Distribution Map")

try:

    map_fig=px.choropleth(
        year_data,
        locations=country_col,
        locationmode="country names",
        color=value_col,
        title="Income Distribution Map"
    )

    st.plotly_chart(map_fig,use_container_width=True)

except:
    st.info("Map visualization not available for this dataset format.")

# ---------------------------------------------------
# COUNTRY TREND
# ---------------------------------------------------

st.subheader("📈 Country Trend")

try:

    trend_fig=px.line(
        country_data,
        x=year_col,
        y=value_col,
        title=f"{selected_country} Trend"
    )

    st.plotly_chart(trend_fig,use_container_width=True)

except:
    st.info("Trend chart unavailable.")

# ---------------------------------------------------
# TOP COUNTRIES
# ---------------------------------------------------

st.subheader("🏆 Top Countries")

try:

    top10=year_data.sort_values(value_col,ascending=False).head(10)

    bar_fig=px.bar(
        top10,
        x=country_col,
        y=value_col,
        title="Top 10 Countries"
    )

    st.plotly_chart(bar_fig,use_container_width=True)

except:
    st.info("Top country chart unavailable.")

# ---------------------------------------------------
# 3D GLOBE STYLE VISUALIZATION
# ---------------------------------------------------

st.subheader("🌐 3D Globe Visualization")

try:

    globe_fig=px.scatter_geo(
        year_data,
        locations=country_col,
        locationmode="country names",
        size=value_col,
        projection="orthographic"
    )

    st.plotly_chart(globe_fig,use_container_width=True)

except:
    st.info("3D globe unavailable.")

# ---------------------------------------------------
# ML FORECAST
# ---------------------------------------------------

st.subheader("🧠 ML Prediction")

try:

    temp=country_data[[year_col,value_col]].dropna()

    X=temp[[year_col]]
    y=temp[value_col]

    model=LinearRegression()
    model.fit(X,y)

    future_year=st.slider("Predict future year",
                          int(min(years)),
                          int(max(years)+20))

    prediction=model.predict([[future_year]])[0]

    st.success(f"Predicted value for {selected_country} in {future_year}: {round(prediction,2)}")

except:
    st.info("Prediction not available.")

# ---------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------

st.subheader("🤖 Automatic Insights")

try:

    st.write(f"• Average value in {selected_year} is {round(avg_value,2)}.")
    st.write(f"• {top_country} has the highest value.")
    st.write(f"• {low_country} has the lowest value.")

except:
    st.write("Insights unavailable.")

# ---------------------------------------------------
# CHAT ASSISTANT
# ---------------------------------------------------

st.subheader("💬 Data Assistant")

question=st.text_input("Ask a question about the data")

if question:

    q=question.lower()

    if "average" in q:
        st.write(f"Average value is {round(avg_value,2)}")

    elif "top" in q:
        st.write(f"Top country is {top_country}")

    elif "lowest" in q:
        st.write(f"Lowest country is {low_country}")

    else:
        st.write("Try asking about average, top country, or lowest country.")

# ---------------------------------------------------
# POWER BI EMBED
# ---------------------------------------------------

st.subheader("📊 Embedded Power BI Dashboard")

powerbi_link=st.text_input("Paste Power BI embed URL")

if powerbi_link:

    st.components.v1.iframe(
        powerbi_link,
        height=600
    )

# ---------------------------------------------------
# PDF REPORT GENERATOR
# ---------------------------------------------------

st.subheader("📄 Generate PDF Report")

if st.button("Create Report"):

    buffer=BytesIO()

    doc=SimpleDocTemplate(buffer)

    styles=getSampleStyleSheet()

    story=[]

    story.append(Paragraph("Global Income Distribution Report",styles["Title"]))
    story.append(Spacer(1,20))

    story.append(Paragraph(f"Year: {selected_year}",styles["Normal"]))
    story.append(Paragraph(f"Average Value: {round(avg_value,2)}",styles["Normal"]))
    story.append(Paragraph(f"Top Country: {top_country}",styles["Normal"]))
    story.append(Paragraph(f"Lowest Country: {low_country}",styles["Normal"]))

    doc.build(story)

    st.download_button(
        "Download PDF",
        buffer.getvalue(),
        file_name="income_report.pdf"
    )
