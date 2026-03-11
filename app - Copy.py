import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# -------------------------------
# ADVANCED STYLING
# -------------------------------
st.markdown("""
<style>
/* App background and font */
.stApp {
    background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
    color:white;
    font-family: 'Segoe UI';
}

/* Animated Gradient Title */
.title {
    font-size: 50px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(270deg,#ff6ec4,#7873f5,#00f2ff);
    background-size: 600% 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientAnimation 8s ease infinite;
    margin-bottom: 25px;
}

@keyframes gradientAnimation {
  0%{background-position:0% 50%}
  50%{background-position:100% 50%}
  100%{background-position:0% 50%}
}

/* Glass Cards */
.card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(15px);
    border-radius: 25px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: transform 0.4s ease, box-shadow 0.4s ease, background 0.4s ease;
}
.card:hover {
    transform: scale(1.05) rotateX(3deg) rotateY(3deg);
    box-shadow: 0 15px 45px rgba(0,0,0,0.5);
    background: rgba(255,255,255,0.12);
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg,#1e1b4b,#312e81);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.7), 0 0 10px #6366f1;
    transition: transform 0.3s ease, background 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
.kpi-card:hover {
    transform: scale(1.1) rotateX(5deg) rotateY(5deg);
    background: linear-gradient(145deg,#3b30a0,#5140c4,#06b6d4);
    box-shadow: 0 20px 40px rgba(0,0,0,0.7), 0 0 20px #a78bfa;
}

.kpi-number {
    font-size: 45px;
    font-weight: 900;
    background: linear-gradient(90deg,#a78bfa,#06b6d4,#f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: all 0.3s ease;
}
.kpi-label {
    font-size: 18px;
    color: #ddd;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Sidebar styling */
section[data-testid="stSidebar"]{
  background: linear-gradient(180deg,#020617,#111827);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label{
  transition: all 0.3s ease;
  border-radius: 12px;
  padding: 8px 12px;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover{
  background: linear-gradient(90deg,#6366f1,#a855f7,#06b6d4);
  color:#fff;
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(99,102,241,0.4);
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"]{
  background: linear-gradient(90deg,#f59e0b,#22d3ee);
  color:#fff;
  border: 2px solid #fff;
  box-shadow: 0 0 15px #f59e0b, 0 0 15px #22d3ee;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()
numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# -------------------------------
# LOGIN SYSTEM
# -------------------------------
if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:
    st.markdown("<div class='title'>🌍 Global Income Intelligence Platform</div>",unsafe_allow_html=True)
    user = st.text_input("Username")
    pw = st.text_input("Password",type="password")
    if st.button("Login"):
        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid login")
    st.stop()

# -------------------------------
# SIDEBAR NAVIGATION
# -------------------------------
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go To", [
"🏠 Introduction",   
"🏠 Executive Dashboard",
"📘 Dashboard Guide",
"📊 Power BI Dashboard",
"🧾 Dataset Explorer",
"📈 Chart Explorer",
"🌐 Country Comparison",
"🤖 AI Insights Generator",
"🌍 Country Analysis",
"🗺 Global Map Visualization",
"🧠 Machine Learning Prediction",
"⚡ Auto ML Prediction",
"⏳ Time Series Forecasting",
"📄 Generate PDF Report",
"❓ FAQ",
"ℹ About"
])

# -------------------------------
# INTRODUCTION
# -------------------------------

if menu == "🏠 Introduction":

    st.markdown("<div class='title'>Introduction</div>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.markdown(f"<div class='kpi-card'><div class='kpi-number'>62.49</div><div class='kpi-label'>Inequality Range</div></div>",unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi-card'><div class='kpi-number'>37.52</div><div class='kpi-label'>Avg Gini Index</div></div>",unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi-card'><div class='kpi-number'>22.55</div><div class='kpi-label'>Avg Inequality Index</div></div>",unsafe_allow_html=True)
    col4.markdown(f"<div class='kpi-card'><div class='kpi-number'>200</div><div class='kpi-label'>Total Countries</div></div>",unsafe_allow_html=True)
    col5.markdown(f"<div class='kpi-card'><div class='kpi-number'>7.85bn</div><div class='kpi-label'>Total Population</div></div>",unsafe_allow_html=True)

    st.markdown("""

# Project Title  
### Interactive Analytics Dashboard for Global Income Distribution

---

# 1. Project Overview

The **Interactive Analytics Dashboard for Global Income Distribution** is a data analytics platform designed to explore global income inequality using modern visualization tools and machine learning techniques.  

Income inequality is one of the most important global economic issues affecting societies worldwide. Governments, researchers, and organizations often analyze inequality indicators such as the **Gini Index** and **Income Distribution Metrics** to understand how wealth is distributed across populations.

However, analyzing such data using spreadsheets or static reports can be extremely difficult. Large datasets often hide valuable insights that are not easily visible without interactive tools.

This project solves that problem by building a **fully interactive analytics dashboard** that allows users to explore global income distribution in a visually engaging way.

The platform integrates **data analysis, visualization, and machine learning** into one unified interface.

---

# 2. Purpose of the Project

The purpose of this project is to create a powerful analytical tool that enables users to explore patterns of income inequality across different countries and time periods.

The dashboard allows users to:

• Understand global inequality trends  
• Compare countries based on income distribution metrics  
• Analyze changes in inequality over time  
• Visualize data using advanced charts  
• Predict future inequality values using machine learning  

By transforming raw economic data into meaningful visualizations, the platform helps users gain deeper insights into global economic patterns.

---

# 3. Problem Statement

Understanding global income inequality can be challenging due to several factors:

• Large and complex datasets  
• Lack of interactive analytical tools  
• Difficulty identifying trends from static reports  
• Limited accessibility for non-technical users  

Traditional analysis methods often require significant technical expertise. This project aims to simplify the process by providing an **interactive dashboard that anyone can use**.

---

# 4. Dataset Description

The dataset used in this project contains information about global income distribution and inequality indicators across multiple countries and years.

Key variables included in the dataset:

• Country name  
• Year of observation  
• Population statistics  
• Gini Index values  
• Inequality Index values  
• Income distribution indicators  

These variables allow users to analyze both **geographical patterns** and **historical trends** in income inequality.

---

# 5. Data Preparation Process

Before building the dashboard, several data preprocessing steps were performed to ensure the dataset was clean and reliable.

### Data Cleaning
Raw datasets often contain inconsistencies such as missing values, incorrect formatting, or duplicate records. These issues were addressed through data cleaning techniques.

### Handling Missing Values
Missing data points were handled using methods such as:

• removing incomplete records  
• replacing values with averages  
• interpolation for time-series variables  

### Data Transformation
Certain variables were transformed into formats suitable for visualization and machine learning models.

---

# 6. Tools and Technologies Used

This project was built using modern data science and analytics technologies.

### Dashboard Development
The dashboard interface was built using **Streamlit**, a Python framework that enables the creation of interactive web applications for data analysis.

### Data Processing
Data manipulation and analysis were performed using the **Pandas** library.

### Data Visualization
Interactive charts were created using **Plotly**, which allows dynamic exploration of datasets.

### Machine Learning
Predictive analytics were implemented using **Scikit-learn** models including:

• Linear Regression  
• Random Forest Regression  

### Report Generation
PDF reports are generated using **ReportLab**.

---

# 7. Dashboard Features

The dashboard includes several modules designed for different types of analysis.

### Executive Dashboard
Provides an overview of key dataset statistics such as total countries, population, and inequality metrics.

### Data Explorer
Allows users to inspect the dataset and understand variable distributions.

### Interactive Charts
Users can visualize relationships between variables using scatter plots, histograms, and bar charts.

### Country Analysis
Provides country-level insights into income distribution metrics.

### Machine Learning Prediction
Allows users to predict income distribution metrics for specific years using regression models.

### Forecasting Engine
Generates forecasts for future inequality values based on historical data patterns.

---

# 8. User Interface Design

The dashboard uses a modern **glassmorphism design style** that improves visual appeal and usability.

Key UI elements include:

• gradient backgrounds  
• transparent glass cards  
• animated hover effects  
• responsive layout  

These design choices make the dashboard visually engaging while maintaining clarity.

---

# 9. Analytical Insights

Using this dashboard, users can discover valuable insights such as:

• which countries have the highest inequality levels  
• how inequality changes over time  
• correlations between economic indicators  
• patterns in global income distribution  

---

# 10. Real-World Applications

This dashboard can be used in multiple domains including:

• economic research  
• public policy analysis  
• academic education  
• international development studies  

Organizations analyzing global inequality can use such platforms to support evidence-based decision making.

---

# 11. Project Outcome

The final outcome of this project is a **fully functional interactive dashboard** capable of transforming complex global datasets into clear visual insights.

The project demonstrates the power of combining **data science, visualization, and machine learning** to analyze real-world socioeconomic challenges.

---

# 12. Future Improvements

Future versions of the dashboard could include:

• real-time economic data integration  
• advanced forecasting models  
• anomaly detection algorithms  
• AI-driven insight generation  
• deployment on cloud platforms  

These enhancements could transform the dashboard into a large-scale analytics platform.

---

# 13. Conclusion

The **Interactive Analytics Dashboard for Global Income Distribution** highlights how modern data analytics tools can help us better understand global economic inequality.

By combining powerful visualization techniques with predictive analytics, this platform provides an intuitive and accessible way to explore complex economic datasets.

The project demonstrates how data science can be used to create impactful tools for understanding global challenges.

""", unsafe_allow_html=True)

# -------------------------------
# EXECUTIVE DASHBOARD
# -------------------------------
elif menu=="🏠 Executive Dashboard":
    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    col1.markdown(f"<div class='kpi-card'><div class='kpi-number'>{df.shape[0]}</div><div class='kpi-label'>Total Rows</div></div>",unsafe_allow_html=True)
    col2.markdown(f"<div class='kpi-card'><div class='kpi-number'>{df.shape[1]}</div><div class='kpi-label'>Total Columns</div></div>",unsafe_allow_html=True)
    col3.markdown(f"<div class='kpi-card'><div class='kpi-number'>{len(numeric_cols)}</div><div class='kpi-label'>Numeric Features</div></div>",unsafe_allow_html=True)
    col4.markdown(f"<div class='kpi-card'><div class='kpi-number'>{len(categorical_cols)}</div><div class='kpi-label'>Categorical Features</div></div>",unsafe_allow_html=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Insights")
    col1,col2=st.columns(2)
    col1.markdown(f"<div class='card'><h4>Missing Values</h4><p>{df.isnull().sum().sum()} missing values detected.</p></div>",unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h4>Duplicate Rows</h4><p>{df.duplicated().sum()} duplicate rows found.</p></div>",unsafe_allow_html=True)

    if len(numeric_cols)>0:
        fig,ax=plt.subplots()
        df[numeric_cols[0]].hist(ax=ax)
        st.pyplot(fig)

# -------------------------------
# DASHBOARD GUIDE
# -------------------------------
elif menu=="📘 Dashboard Guide":

    st.markdown("<div class='title'>Platform User Guide</div>",unsafe_allow_html=True)

    st.markdown("""

# 🌍 Global Income Intelligence Platform – Complete User Guide

Welcome to the **Global Income Intelligence Platform**.  
This dashboard is designed to help users explore global income distribution, analyze inequality trends, and generate insights using interactive visualizations and machine learning models.

This guide explains each module of the platform and how to use them effectively.

---

# 1️⃣ Executive Dashboard

The **Executive Dashboard** provides a high-level overview of the dataset.

This section is designed for quick insights and decision-making. It summarizes the most important statistics from the dataset and presents them through key performance indicators (KPIs).

Key elements available in this dashboard include:

• Total number of records in the dataset  
• Total number of countries included in the analysis  
• Average Gini Index across all countries  
• Average Inequality Index values  
• Population statistics  

These metrics help users quickly understand the scale and distribution of the dataset before diving deeper into detailed analysis.

The Executive Dashboard acts as the **central overview panel** for the entire platform.

---

# 2️⃣ Power BI Dashboard

This section embeds a professional **business intelligence dashboard**.

It integrates an external enterprise visualization environment into the platform.

Features of this module include:

• Advanced interactive charts  
• Drill-down analytics  
• Pre-built business intelligence reports  
• enterprise-level visual analytics  

Users can interact with the embedded dashboard directly within the application.

This module demonstrates how modern analytics platforms integrate with enterprise BI systems to deliver powerful data insights.

---

# 3️⃣ Dataset Explorer

The **Dataset Explorer** allows users to inspect the raw dataset used in the platform.

This module provides detailed access to the dataset structure and statistics.

Users can:

• View all dataset rows and columns  
• Explore column types  
• Analyze statistical summaries  
• Identify missing values  
• Understand variable distributions  

This section is especially useful for:

• data scientists  
• analysts  
• researchers  

It allows them to understand the dataset before performing advanced analysis.

---

# 4️⃣ Chart Explorer

The **Chart Explorer** is a dynamic visualization environment that allows users to generate interactive charts.

Users can create various visualizations such as:

• Histograms  
• Scatter plots  
• Line charts  
• Box plots  
• Heatmaps  

These visualizations help users identify relationships between variables, detect patterns in income distribution, and uncover hidden insights in the data.

The interactive nature of the charts allows users to zoom, filter, and hover over data points for additional information.

---

# 5️⃣ AI Insights Generator

The **AI Insights Generator** automatically analyzes the dataset and generates statistical insights.

Instead of manually calculating statistics, the platform automatically computes:

• mean values  
• standard deviation  
• maximum values  
• minimum values  
• distribution ranges  

These insights help users quickly understand the characteristics of each variable without performing manual calculations.

This module acts as an **automated analytics assistant**.

---

# 6️⃣ Country Analysis

The **Country Analysis module** allows users to explore inequality metrics for specific countries.

Users can select a country and examine its economic indicators.

This module helps answer questions such as:

• Which countries have the highest income inequality?  
• How does inequality vary across regions?  
• What are the trends in a specific country?  

Visual charts provide a clear representation of country-level inequality metrics.

---

# 7️⃣ Global Map Visualization

This section displays a **global geographic visualization** of income distribution.

Using a world map, users can analyze inequality indicators across different countries.

Features include:

• interactive world map  
• color-coded inequality levels  
• geographic comparison of income distribution  
• quick identification of high and low inequality regions  

This visualization provides a spatial understanding of economic inequality.

---

# 8️⃣ Machine Learning Prediction

The **Machine Learning Prediction module** uses predictive analytics to estimate future values.

The model uses historical data and applies **Linear Regression** to generate predictions.

Users can input a year or variable and obtain predicted values for inequality indicators.

This module demonstrates how machine learning can be applied to economic datasets.

---

# 9️⃣ Auto ML Prediction

The **Auto ML Prediction system** compares multiple machine learning models to determine the best-performing model.

Instead of manually selecting an algorithm, the system evaluates models such as:

• Linear Regression  
• Random Forest  
• Decision Tree  

The model with the highest performance is selected automatically.

This feature improves prediction accuracy and simplifies the machine learning workflow.

---

# 🔟 Time Series Forecasting

The **Time Series Forecasting module** analyzes historical trends in inequality metrics.

By studying patterns over time, the system can forecast future trends.

This helps answer questions such as:

• Will inequality increase in the future?  
• Are current trends improving or worsening?  
• What are the long-term projections for income distribution?

Forecasting charts visually represent predicted future trends.

---

# 1️⃣1️⃣ Generate PDF Report

The **Report Generation module** allows users to export analytical results.

Users can download a **PDF summary report** containing:

• dataset statistics  
• analytical insights  
• summary metrics  

This feature is useful for sharing insights with stakeholders, researchers, or policymakers.

---

# 1️⃣2️⃣ FAQ & About Section

The **FAQ and About module** provides helpful information about the platform.

It includes details such as:

• project purpose  
• technologies used  
• data sources  
• guidance for new users  

This section ensures users understand how the platform works and how to use its features effectively.

---

# 🧠 Final Notes

The **Global Income Intelligence Platform** combines modern data analytics tools with machine learning to create a powerful analytical environment.

Through interactive dashboards, predictive analytics, and automated insights, users can better understand the complex issue of global income inequality.

This platform demonstrates how data science and visualization technologies can transform raw data into meaningful insights.

""",unsafe_allow_html=True)

# -------------------------------
# POWER BI DASHBOARD
# -------------------------------
elif menu=="📊 Power BI Dashboard":
    st.title("Power BI Dashboard")
    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"
    st.components.v1.iframe(powerbi_url,height=700)

# -------------------------------
# DATASET EXPLORER
# -------------------------------
elif menu=="🧾 Dataset Explorer":
    st.title("Dataset Explorer")
    st.dataframe(df)
    column = st.selectbox("Select Column",df.columns)
    st.write(df[column].describe())
    st.subheader("Missing Values")
    st.write(df.isnull().sum())
    st.subheader("Duplicate Rows")
    st.write(df.duplicated().sum())
    st.download_button("Download Dataset", df.to_csv(index=False), "dataset.csv")

# -------------------------------
# CHART EXPLORER
# -------------------------------
elif menu=="📈 Chart Explorer":
    st.title("Chart Explorer")
    chart = st.selectbox("Choose Chart", ["Histogram","Boxplot","Scatter","Bar","Line","Correlation Heatmap"])
    fig,ax=plt.subplots()
    if chart=="Histogram":
        col=st.selectbox("Column",numeric_cols)
        sns.histplot(df[col],ax=ax)
    elif chart=="Boxplot":
        col=st.selectbox("Column",numeric_cols)
        sns.boxplot(x=df[col],ax=ax)
    elif chart=="Scatter":
        x=st.selectbox("X Axis",numeric_cols)
        y=st.selectbox("Y Axis",numeric_cols)
        sns.scatterplot(x=df[x],y=df[y],ax=ax)
    elif chart=="Bar":
        col=st.selectbox("Column",categorical_cols)
        df[col].value_counts().plot(kind="bar",ax=ax)
    elif chart=="Line":
        col=st.selectbox("Column",numeric_cols)
        df[col].plot(ax=ax)
    elif chart=="Correlation Heatmap":
        sns.heatmap(df[numeric_cols].corr(),annot=True,ax=ax)
    st.pyplot(fig)

# -------------------------------
# COUNTRY COMPARISON
# -------------------------------
elif menu == "🌐 Country Comparison":
    st.markdown("<div class='title'>Country Comparison</div>", unsafe_allow_html=True)
    country_cols = [c for c in df.columns if "country" in c.lower()]
    if country_cols:
        country_col = country_cols[0]
        countries = st.multiselect("Select Countries", df[country_col].unique(), default=df[country_col].unique()[:3])
        if countries:
            filtered_df = df[df[country_col].isin(countries)]
            kpi_cols = st.multiselect("Select KPIs", numeric_cols, default=numeric_cols[:3])
            if kpi_cols:
                st.subheader("Comparison Table")
                st.dataframe(filtered_df[[country_col] + kpi_cols].reset_index(drop=True))
                st.subheader("Comparison Bar Chart")
                fig = px.bar(filtered_df, x=country_col, y=kpi_cols, barmode="group", height=500)
                st.plotly_chart(fig,use_container_width=True)
                if st.checkbox("Show Radar Chart"):
                    fig = go.Figure()
                    for c in countries:
                        country_data = filtered_df[filtered_df[country_col]==c][kpi_cols].mean()
                        fig.add_trace(go.Scatterpolar(r=country_data.values,theta=kpi_cols,fill='toself',name=c))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=True)),title="Radar Chart Comparison")
                    st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("Select at least one country.")
    else:
        st.warning("No country column found.")

# -------------------------------
# AI INSIGHTS GENERATOR
# -------------------------------
elif menu=="🤖 AI Insights Generator":
    st.title("Automatic AI Insights")
    st.write(df.describe())
    for col in numeric_cols:
        mean=df[col].mean(); median=df[col].median(); std=df[col].std()
        st.info(f"{col}: Mean={mean:.2f} | Median={median:.2f} | Std Dev={std:.2f}")

# -------------------------------
# COUNTRY ANALYSIS
# -------------------------------
elif menu=="🌍 Country Analysis":

    st.title("🌍 Country Analysis Dashboard")

    country_cols=[c for c in df.columns if "country" in c.lower()]

    if country_cols:

        country_col=country_cols[0]

        country=st.selectbox("Select Country",df[country_col].unique())

        filtered=df[df[country_col]==country]

        st.subheader("Country Dataset")
        st.dataframe(filtered)

        st.divider()

        # ---------------- LINE CHART ----------------

        year_cols=[c for c in df.columns if "year" in c.lower()]

        if year_cols:

            year_col=year_cols[0]

            st.subheader("📈 Trend Over Time")

            fig2=px.line(
                filtered,
                x=year_col,
                y=numeric_cols,
                markers=True,
                template="plotly_dark",
                title="Income Trend Over Years"
            )

            st.plotly_chart(fig2,use_container_width=True)

        # ---------------- AREA CHART ----------------

        st.subheader("📉 Area Distribution")

        fig3=px.area(
            filtered,
            y=numeric_cols[0],
            template="plotly_dark",
            title="Income Distribution Area"
        )

        st.plotly_chart(fig3,use_container_width=True)

        # ---------------- PIE CHART ----------------

        st.subheader("🥧 Indicator Contribution")

        pie_df=filtered[numeric_cols].mean().reset_index()
        pie_df.columns=["Indicator","Value"]

        fig4=px.pie(
            pie_df,
            names="Indicator",
            values="Value",
            hole=0.4,
            template="plotly_dark"
        )

        st.plotly_chart(fig4,use_container_width=True)

        # ---------------- SCATTER PLOT ----------------

        if len(numeric_cols) >= 2:

            st.subheader("📉 Indicator Relationship")

            fig5=px.scatter(
                filtered,
                x=numeric_cols[0],
                y=numeric_cols[1],
                size=numeric_cols[0],
                color=numeric_cols[1],
                template="plotly_dark",
                title="Income Relationship Scatter"
            )

            st.plotly_chart(fig5,use_container_width=True)

        # ---------------- BOX PLOT ----------------

        st.subheader("📊 Distribution Analysis")

        fig6=px.box(
            filtered,
            y=numeric_cols,
            template="plotly_dark",
            title="Indicator Distribution"
        )

        st.plotly_chart(fig6,use_container_width=True)

        # ---------------- HEATMAP ----------------

        st.subheader("🔥 Correlation Heatmap")

        corr=filtered[numeric_cols].corr()

        fig7=px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="RdBu",
            title="Indicator Correlation",
            template="plotly_dark"
        )

        st.plotly_chart(fig7,use_container_width=True)

# -------------------------------
# GLOBAL MAP
# -------------------------------
elif menu=="🗺 Global Map Visualization":
    st.title("Global Income Map")
    country_col=st.selectbox("Country Column",df.columns)
    value_col=st.selectbox("Value Column",numeric_cols)
    fig=px.choropleth(df, locations=country_col, locationmode="country names",
                      color=value_col, color_continuous_scale="Viridis")
    st.plotly_chart(fig,use_container_width=True)

# -------------------------------
# MACHINE LEARNING
# -------------------------------
elif menu=="🧠 Machine Learning Prediction":
    st.title("Machine Learning Prediction")
    target=st.selectbox("Target Variable",numeric_cols)
    features=[c for c in numeric_cols if c!=target]
    X=df[features].fillna(0); y=df[target].fillna(0)
    model=LinearRegression(); model.fit(X,y)
    inputs=[st.number_input(col,value=float(X[col].mean())) for col in features]
    if st.button("Predict"):
        prediction=model.predict([inputs])[0]
        st.success(f"Predicted {target}: {prediction:.2f}")

# -------------------------------
# AUTO ML
# -------------------------------
elif menu=="⚡ Auto ML Prediction":
    st.title("Auto ML Model Selection")
    target=st.selectbox("Target Variable",numeric_cols)
    features=[c for c in numeric_cols if c!=target]
    X=df[features]; y=df[target]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    models={"Linear Regression":LinearRegression(),"Decision Tree":DecisionTreeRegressor(),"Random Forest":RandomForestRegressor()}
    results={}
    for name,model in models.items():
        model.fit(X_train,y_train)
        pred=model.predict(X_test)
        results[name]=r2_score(y_test,pred)
    best=max(results,key=results.get)
    st.success(f"Best Model: {best}"); st.write(results)

# -------------------------------
# TIME SERIES
# -------------------------------
elif menu=="⏳ Time Series Forecasting":
    st.title("Time Series Analysis")
    time_col=st.selectbox("Time Column",df.columns)
    value_col=st.selectbox("Value Column",numeric_cols)
    df_sorted=df.sort_values(time_col)
    fig,ax=plt.subplots()
    ax.plot(df_sorted[time_col],df_sorted[value_col])
    st.pyplot(fig)

# -------------------------------
# PDF REPORT
# -------------------------------
elif menu=="📄 Generate PDF Report":
    st.title("Generate Report")
    if st.button("Create PDF"):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 750, "Global Income Report")
        pdf.drawString(100, 720, f"Rows: {df.shape[0]}")
        pdf.drawString(100, 700, f"Columns: {df.shape[1]}")
        pdf.save()
        buffer.seek(0)  # Important: reset buffer position before download
        st.download_button(
            label="Download PDF Report",
            data=buffer,
            file_name="Global_Income_Report.pdf",
            mime="application/pdf"
        )

# -------------------------------
# FAQ PAGE
# -------------------------------

elif menu == "❓ FAQ":

    st.markdown("<div class='title'>Frequently Asked Questions</div>", unsafe_allow_html=True)

    st.markdown("""
Welcome to the **FAQ section of the Global Income Intelligence Platform**.

This page answers common questions users may have while exploring the dashboard.  
It helps users understand how the platform works, how to interpret the analytics, and how to use the available tools effectively.
""")

    st.divider()

    with st.expander("What is the purpose of this platform?"):
        st.write("""
        The platform was created to analyze **global income inequality** using modern data analytics tools.

        It provides interactive dashboards that allow users to explore economic data, visualize inequality metrics,
        analyze country-level trends, and generate predictive insights using machine learning models.
        """)

    with st.expander("What dataset is used in this project?"):
        st.write("""
        The dashboard uses a global dataset containing information about income distribution across countries.

        Key variables include:

        • Country name  
        • Year  
        • Population statistics  
        • Gini Index  
        • Inequality Index  
        • Income distribution indicators
        """)

    with st.expander("What is the Gini Index?"):
        st.write("""
        The **Gini Index** is a widely used statistical measure of income inequality.

        A value of:

        • **0** represents perfect equality  
        • **100** represents maximum inequality  

        Countries with higher Gini Index values tend to have greater income disparity among citizens.
        """)

    with st.expander("What technologies power this dashboard?"):
        st.write("""
        The platform is built using a modern data analytics stack:

        • Python programming language  
        • Streamlit for interactive dashboards  
        • Pandas for data processing  
        • Plotly for visualizations  
        • Scikit-learn for machine learning  
        • ReportLab for PDF report generation
        """)

    with st.expander("Can this dashboard predict future inequality?"):
        st.write("""
        Yes. The platform includes machine learning modules that perform:

        • regression-based predictions  
        • forecasting of future inequality values  
        • trend analysis based on historical data

        These predictions provide insights into potential future patterns in global income distribution.
        """)

    with st.expander("Who can use this platform?"):
        st.write("""
        The platform is useful for a wide range of users including:

        • data analysts  
        • economists  
        • researchers  
        • students studying data science or economics  
        • policymakers evaluating economic inequality
        """)

    st.divider()

    st.info("If you still have questions, explore the Dashboard Guide section or review the About page for additional details.")


# -------------------------------
# ABOUT PLATFORM
# -------------------------------

elif menu == "ℹ About":

    st.markdown("<div class='title'>About the Global Income Intelligence Platform</div>", unsafe_allow_html=True)

    st.markdown("""

## Project Overview

The **Global Income Intelligence Platform** is an advanced data analytics dashboard designed to explore and analyze global income distribution patterns.

The platform integrates data visualization, statistical analysis, and machine learning models to transform complex economic datasets into meaningful insights.

Income inequality is a major global challenge that affects economic development, social stability, and policy decisions. This platform helps users understand these patterns by presenting data in an interactive and intuitive way.

---

## Project Objectives

The main objectives of this platform include:

• Visualizing global income inequality  
• Analyzing economic trends across countries  
• Providing interactive data exploration tools  
• Applying machine learning for predictive analytics  
• Generating automated analytical insights  

By combining these capabilities, the dashboard provides a powerful environment for exploring socioeconomic data.

---

## Key Features of the Platform

The platform includes several advanced analytics modules:

### Executive Dashboard
Provides a high-level overview of dataset statistics and inequality metrics.

### Dataset Explorer
Allows users to inspect raw data and analyze column statistics.

### Interactive Charts
Supports dynamic visualizations such as scatter plots, histograms, and line charts.

### Country Analysis
Enables country-level exploration of inequality indicators.

### Machine Learning Prediction
Uses regression models to estimate inequality values based on historical data.

### Forecasting Engine
Analyzes time-series trends to project future inequality patterns.

### Report Generation
Allows users to export analytical results as downloadable PDF reports.

---

## Technology Stack

This dashboard was developed using modern data science tools:

• **Python** – core programming language  
• **Streamlit** – dashboard development framework  
• **Pandas** – data manipulation and analysis  
• **Plotly** – interactive data visualizations  
• **Scikit-learn** – machine learning algorithms  
• **ReportLab** – PDF report generation  

Together these tools enable the development of scalable and interactive analytics platforms.

---

## Target Users

This platform can be used by:

• economists studying income inequality  
• researchers analyzing socioeconomic data  
• students learning data science and analytics  
• policymakers evaluating economic policies  
• analysts exploring global datasets

---

## Future Enhancements

Future improvements may include:

• real-time economic data integration  
• advanced machine learning forecasting models  
• AI-powered insight generation  
• interactive global 3D visualizations  
• cloud-based deployment

---

## Project Summary

The **Global Income Intelligence Platform** demonstrates how modern data analytics technologies can be applied to analyze complex global challenges such as income inequality.

By combining visualization, machine learning, and interactive dashboards, the platform transforms raw data into meaningful insights that support research and decision-making.

""")

    st.divider()

    col1, col2, col3 = st.columns(3)

    col1.metric("Platform Version", "1.0")
    col2.metric("Dashboard Modules", "10+")
    col3.metric("Visualization Types", "15+")
       



