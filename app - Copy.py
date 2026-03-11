import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# -------------------------------
# ADVANCED 3D UI STYLE
# -------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
color:white;
font-family: 'Segoe UI';
}

/* Title */
.title{
font-size:45px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#a855f7,#6366f1,#06b6d4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:25px;
transition: all 0.3s ease;
}

/* Glass Cards */
.card{
background: rgba(255,255,255,0.08);
backdrop-filter: blur(12px);
border-radius:20px;
padding:25px;
box-shadow:0 10px 30px rgba(0,0,0,0.5);
transition: transform 0.3s ease, background 0.3s ease;
}

.card:hover{
transform: translateY(-10px) scale(1.03) rotateX(3deg) rotateY(3deg);
background: rgba(255,255,255,0.12);
}

/* KPI Cards */
.kpi-card{
background: linear-gradient(145deg,#1e1b4b,#312e81);
border-radius:18px;
padding:25px;
text-align:center;
box-shadow:0 12px 35px rgba(0,0,0,0.6);
transition: transform 0.3s ease, background 0.3s ease, color 0.3s ease;
cursor:pointer;
}

.kpi-card:hover{
transform: scale(1.08) rotateX(5deg) rotateY(5deg);
background: linear-gradient(145deg,#3b30a0,#5140c4);
color:#fff;
}

.kpi-number{
font-size:40px;
font-weight:800;
background: linear-gradient(90deg,#a78bfa,#06b6d4);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
transition: all 0.3s ease;
}

.kpi-card:hover .kpi-number{
background: linear-gradient(90deg,#facc15,#22d3ee);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.kpi-label{
font-size:16px;
color:#ddd;
transition: color 0.3s ease;
}

.kpi-card:hover .kpi-label{
color:#fff;
}

/* Sidebar with gradient hover for options */
section[data-testid="stSidebar"]{
background: linear-gradient(180deg,#020617,#111827);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label{
transition: background 0.3s ease, color 0.3s ease;
border-radius: 10px;
padding: 5px 10px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover{
background: linear-gradient(90deg,#6366f1,#a855f7,#06b6d4);
color:#fff;
transform: scale(1.05);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label[aria-checked="true"]{
background: linear-gradient(90deg,#f59e0b,#22d3ee);
color:#fff;
}

</style>
""",unsafe_allow_html=True)

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

    user=st.text_input("Username")
    pw=st.text_input("Password",type="password")

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

menu = st.sidebar.radio(
"Go To",
[
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
]
)

# -------------------------------
# INTRODUCTION SECTION
# -------------------------------
if menu == "🏠 Introduction":
    st.markdown("<div class='title'>Introduction</div>", unsafe_allow_html=True)

    # Neomorphic KPI Cards at the top
    st.markdown("""
    <style>
    .neo-card {
        background: #1e1e2f;
        border-radius: 15px;
        padding: 25px;
        margin: 10px 5px;
        color: white;
        text-align: center;
        box-shadow: 6px 6px 12px #161625, -6px -6px 12px #27283d;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        cursor: default;
        user-select: none;
        transition: box-shadow 0.3s ease;
    }
    .neo-card:hover {
        box-shadow: inset 6px 6px 12px #161625, inset -6px -6px 12px #27283d;
        color: #f0f8ff;
    }
    .neo-number {
        font-weight: 900;
        font-size: 40px;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
        background: linear-gradient(90deg, #a78bfa, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .neo-label {
        font-weight: 600;
        font-size: 14px;
        color: #b0b7c3;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown(f"""<div class="neo-card"><div class="neo-number">62.49</div><div class="neo-label">Inequality Range</div></div>""", unsafe_allow_html=True)
    col2.markdown(f"""<div class="neo-card"><div class="neo-number">37.52</div><div class="neo-label">Avg Gini Index</div></div>""", unsafe_allow_html=True)
    col3.markdown(f"""<div class="neo-card"><div class="neo-number">22.55</div><div class="neo-label">Avg Inequality Index</div></div>""", unsafe_allow_html=True)
    col4.markdown(f"""<div class="neo-card"><div class="neo-number">200</div><div class="neo-label">Total Countries</div></div>""", unsafe_allow_html=True)
    col5.markdown(f"""<div class="neo-card"><div class="neo-number">7.85bn</div><div class="neo-label">Total Updated Population</div></div>""", unsafe_allow_html=True)

    # Project Information below the cards
    st.markdown("""
### Project Title: Interactive Analytics Dashboard for Global Income Distribution

### Project Statement and Outcomes:
The Interactive Analytics Dashboard for Global Income Distribution project aims to develop an interactive Power BI dashboard that visualizes income inequality data across various countries and regions. This project involves collecting, preprocessing, and structuring global income distribution and economic data to enable effective visualization. 

The dashboard will provide users with insights into income disparities over time, country-wise comparisons, and patterns of inequality globally. The outcome will be a user-friendly dashboard, embedded within a Streamlit web application, offering an intuitive interface for economists, researchers, policymakers, and the general public. This platform will help users explore global income inequality, understand disparities across different regions, and analyze trends in wealth distribution. The project will conclude with comprehensive testing to ensure dashboard accuracy and usability, supported by detailed documentation for future reference and enhancements.
""", unsafe_allow_html=True)

# -------------------------------
# EXECUTIVE DASHBOARD
# -------------------------------

if menu=="🏠 Executive Dashboard":

    st.markdown("<div class='title'>Executive Dashboard</div>",unsafe_allow_html=True)

    col1,col2,col3,col4=st.columns(4)

    col1.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{df.shape[0]}</div>
    <div class="kpi-label">Total Rows</div>
    </div>
    """,unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{df.shape[1]}</div>
    <div class="kpi-label">Total Columns</div>
    </div>
    """,unsafe_allow_html=True)

    col3.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{len(numeric_cols)}</div>
    <div class="kpi-label">Numeric Features</div>
    </div>
    """,unsafe_allow_html=True)

    col4.markdown(f"""
    <div class="kpi-card">
    <div class="kpi-number">{len(categorical_cols)}</div>
    <div class="kpi-label">Categorical Features</div>
    </div>
    """,unsafe_allow_html=True)

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    st.subheader("Dataset Insights")

    col1,col2=st.columns(2)

    col1.markdown(f"""
    <div class="card">
    <h4>Missing Values</h4>
    <p>{df.isnull().sum().sum()} missing values detected.</p>
    </div>
    """,unsafe_allow_html=True)

    col2.markdown(f"""
    <div class="card">
    <h4>Duplicate Rows</h4>
    <p>{df.duplicated().sum()} duplicate rows found.</p>
    </div>
    """,unsafe_allow_html=True)

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
### 🌍 Global Income Intelligence Platform Guide
This guide explains each module in the system.

**Executive Dashboard**: High-level dataset overview and KPIs.  
**Power BI Dashboard**: Enterprise-grade BI embed.  
**Dataset Explorer**: Inspect columns, statistics, missing values.  
**Chart Explorer**: Multiple visualizations (histogram, scatter, heatmap).  
**AI Insights Generator**: Auto statistics for numeric columns.  
**Country Analysis**: Filter and visualize per country.  
**Global Map Visualization**: Interactive choropleth map.  
**Machine Learning Prediction**: Linear Regression predictions.  
**Auto ML Prediction**: Compare multiple models.  
**Time Series Forecasting**: Trend analysis.  
**Generate PDF Report**: Download dataset summary.  
**FAQ**: Platform guidance.  
**About**: Technology stack details.
""")

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

    # Automatically detect country column
    country_cols = [c for c in df.columns if "country" in c.lower()]
    if not country_cols:
        st.warning("No country column found in the dataset.")
    else:
        country_col = country_cols[0]

        # User selects multiple countries
        countries = st.multiselect(
            "Select Countries to Compare",
            options=df[country_col].unique(),
            default=df[country_col].unique()[:3]
        )

        if countries:
            filtered_df = df[df[country_col].isin(countries)]

            # Select KPIs to compare
            kpi_cols = st.multiselect(
                "Select KPIs / Numeric Columns to Compare",
                options=numeric_cols,
                default=numeric_cols[:3]
            )

            if kpi_cols:
                st.subheader("Comparison Table")
                st.dataframe(filtered_df[[country_col] + kpi_cols].reset_index(drop=True))

                st.subheader("Comparison Bar Chart")
                fig = px.bar(
                    filtered_df,
                    x=country_col,
                    y=kpi_cols,
                    barmode="group",
                    height=500,
                    title="Country-wise KPI Comparison"
                )
                st.plotly_chart(fig, use_container_width=True)

                # Optional: Radar chart
                if st.checkbox("Show Radar Chart"):
                    import plotly.graph_objects as go

                    fig = go.Figure()
                    for c in countries:
                        country_data = filtered_df[filtered_df[country_col] == c][kpi_cols].mean()
                        fig.add_trace(go.Scatterpolar(
                            r=country_data.values,
                            theta=kpi_cols,
                            fill='toself',
                            name=c
                        ))

                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True)),
                        showlegend=True,
                        title="Radar Chart Comparison"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select at least one KPI to compare.")
        else:
            st.info("Please select at least one country to compare.")

# -------------------------------
# AI INSIGHTS GENERATOR
# -------------------------------

elif menu=="🤖 AI Insights Generator":
    st.title("Automatic AI Insights")
    st.write(df.describe())
    for col in numeric_cols:
        mean=df[col].mean()
        median=df[col].median()
        std=df[col].std()
        st.info(f"{col}: Mean={mean:.2f} | Median={median:.2f} | Std Dev={std:.2f}")

# -------------------------------
# COUNTRY ANALYSIS
# -------------------------------

elif menu=="🌍 Country Analysis":
    st.title("Country Analysis")
    country_cols=[c for c in df.columns if "country" in c.lower()]
    if country_cols:
        country_col=country_cols[0]
        country=st.selectbox("Select Country",df[country_col].unique())
        filtered=df[df[country_col]==country]
        st.dataframe(filtered)
        fig=px.bar(filtered,y=numeric_cols[0])
        st.plotly_chart(fig,use_container_width=True)

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
    X=df[features].fillna(0)
    y=df[target].fillna(0)
    model=LinearRegression()
    model.fit(X,y)
    inputs=[]
    for col in features:
        val=st.number_input(col,value=float(X[col].mean()))
        inputs.append(val)
    if st.button("Predict"):
        prediction=model.predict([inputs])[0]
        st.success(f"Predicted {target}: {prediction}")

# -------------------------------
# AUTO ML
# -------------------------------

elif menu=="⚡ Auto ML Prediction":
    st.title("Auto ML Model Selection")
    target=st.selectbox("Target Variable",numeric_cols)
    features=[c for c in numeric_cols if c!=target]
    X=df[features]
    y=df[target]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
    models={
        "Linear Regression":LinearRegression(),
        "Decision Tree":DecisionTreeRegressor(),
        "Random Forest":RandomForestRegressor()
    }
    results={}
    for name,model in models.items():
        model.fit(X_train,y_train)
        pred=model.predict(X_test)
        score=r2_score(y_test,pred)
        results[name]=score
    best=max(results,key=results.get)
    st.success(f"Best Model: {best}")
    st.write(results)

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
        buffer=io.BytesIO()
        pdf=canvas.Canvas(buffer)
        pdf.drawString(100,750,"Global Income Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")
        pdf.save()
        st.download_button("Download Report", buffer.getvalue(), "report.pdf", "application/pdf")

# -------------------------------
# FAQ
# -------------------------------

elif menu=="❓ FAQ":
    st.title("Frequently Asked Questions")
    st.markdown("""
**What does this platform do?**  
Provides analytics and ML insights for income datasets.

**What ML algorithms are used?**  
Linear Regression, Decision Tree, Random Forest.

**Can I visualize data?**  
Yes, multiple charts and maps are supported.

**Can I export reports?**  
Yes, PDF reports and dataset downloads are available.
""")

# -------------------------------
# ABOUT
# -------------------------------

elif menu=="ℹ About":
    st.title("About Platform")
    st.write("""
Global Income Intelligence Platform built with:

• Python  
• Streamlit  
• Machine Learning  
• Plotly Visualization  
• Power BI Integration
""")


