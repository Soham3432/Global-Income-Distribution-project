import streamlit as st
from datetime import datetime
import os

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="Global Income Distribution Analytics",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------
# DARK PURPLE UI
# --------------------------------

st.markdown("""
<style>

body{
background:linear-gradient(135deg,#0f001f,#2a0055,#3f007a);
color:white;
}

.stApp{
background:linear-gradient(135deg,#0f001f,#2a0055,#3f007a);
}

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#150033,#3a0066);
}

.card{
background:linear-gradient(145deg,#6a11cb,#2575fc);
padding:25px;
border-radius:15px;
text-align:center;
font-weight:bold;
box-shadow:0px 8px 25px rgba(0,0,0,0.7);
margin-bottom:15px;
}

.section{
background:rgba(255,255,255,0.05);
padding:30px;
border-radius:15px;
margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOGIN
# --------------------------------

def login():

    st.title("🌍 Global Income Distribution Analytics Platform")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged = True
            st.success("Login successful")

        else:
            st.error("Invalid login")


if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    login()
    st.stop()

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("🌍 Analytics Platform")

page = st.sidebar.radio(
"Navigation",
[
"Executive Overview",
"Interactive Dashboard",
"Charts Explanation",
"Dashboard Guide",
"FAQ",
"Feedback"
]
)

# --------------------------------
# EXECUTIVE OVERVIEW
# --------------------------------

if page == "Executive Overview":

    st.title("Global Income Distribution Analytics")

    st.markdown("""
This platform analyzes **global income inequality and population distribution**  
using economic indicators such as **Gini Index, Palma Ratio, and Income Share**.

The project integrates **data visualization, economic analysis, and interactive dashboards**
to help users understand inequality trends across countries and regions.
""")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.markdown('<div class="card"><h3>62.49</h3>Inequality Range</div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><h3>37.52</h3>Average Gini Index</div>',unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card"><h3>22.55</h3>Average Inequality Index</div>',unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card"><h3>200</h3>Total Countries</div>',unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="card"><h3>7.85B</h3>Total Population</div>',unsafe_allow_html=True)

    st.markdown("""
### Key Objectives

• Analyze income inequality across global regions  
• Identify countries with highest inequality  
• Compare regional income distribution  
• Track inequality trends over time  

This dashboard helps **policy makers, economists, and researchers**
explore inequality data interactively.
""")

# --------------------------------
# DASHBOARD
# --------------------------------

elif page == "Interactive Dashboard":

    st.title("📊 Global Income Dashboard")

    st.markdown("""
The dashboard below provides an **interactive view of global income inequality**.

You can:

• Filter by income group  
• Filter by region  
• Filter by year  
• Explore country-level insights  
• Compare inequality metrics
""")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,width=1400,height=800)

# --------------------------------
# CHART EXPLANATIONS
# --------------------------------

elif page == "Charts Explanation":

    st.title("📊 Detailed Chart Explanations")

    chart = st.selectbox(
    "Select a chart to explore",
    [
    "Country Distribution by Income Group",
    "Richest 20% Income Share by Region",
    "Palma Ratio by World Bank Group",
    "Top 5 Countries by Inequality",
    "Global Gini Index Trend",
    "Categories by Inequality Level"
    ])

    if chart == "Country Distribution by Income Group":

        st.header("Country Distribution by Income Group")

        st.markdown("""
### What This Chart Shows

This chart shows how countries are distributed across **different income groups**.

The categories include:

• High Income  
• Upper Middle Income  
• Lower Middle Income  
• Low Income

### Why It Matters

Understanding how countries are distributed economically helps identify:

• Global development patterns  
• Economic inequality between nations  
• Regional economic disparities

### Insights from the Dashboard

Most countries fall into **middle income categories**, showing that
many economies are still developing rather than fully developed.
""")

    elif chart == "Richest 20% Income Share by Region":

        st.header("Richest 20% Income Share by Region")

        st.markdown("""
### Chart Overview

This visualization shows how much income is controlled by the **richest 20% of the population**
in different global regions.

### Interpretation

Higher values indicate **stronger wealth concentration**.

### Key Insight

Regions with high concentration indicate **economic imbalance
where wealth is distributed unevenly among citizens**.
""")

    elif chart == "Palma Ratio by World Bank Group":

        st.header("Palma Ratio by World Bank Group")

        st.markdown("""
### What is Palma Ratio?

Palma Ratio compares:

Richest 10% income share vs Poorest 40% income share.

### Why It Is Important

It highlights **income distribution imbalance**.

Higher ratio means:

• Greater inequality  
• Wealth concentration in top earners
""")

    elif chart == "Top 5 Countries by Inequality":

        st.header("Top 5 Countries by Inequality")

        st.markdown("""
### Chart Description

This chart identifies the **five countries with the highest inequality levels**.

### Why It Matters

These countries may require:

• Economic reforms  
• Social welfare programs  
• Policy interventions
""")

    elif chart == "Global Gini Index Trend":

        st.header("Global Gini Index Trend")

        st.markdown("""
### Chart Overview

The Gini Index trend shows how **global inequality has evolved over time**.

### Interpretation

Increasing values indicate rising inequality,
while decreasing values indicate more balanced income distribution.
""")

    elif chart == "Categories by Inequality Level":

        st.header("Categories by Inequality Level")

        st.markdown("""
### Chart Overview

Countries are grouped into:

• Low Inequality  
• Medium Inequality  
• High Inequality  
• Very High Inequality

### Insight

Most countries fall into **medium inequality levels**, indicating
moderate economic imbalance globally.
""")

# --------------------------------
# DASHBOARD GUIDE
# --------------------------------

elif page == "Dashboard Guide":

    st.title("📘 Complete Dashboard Guide")

    st.markdown("""
### 1. Filters

At the top of the dashboard you will see filters:

• Income Classification  
• Inequality Category  
• Census Year  
• World Bank Region  

These filters allow you to **focus on specific countries or regions**.

---

### 2. KPI Cards

KPI cards summarize the most important indicators:

• Inequality Range  
• Average Gini Index  
• Average Inequality Index  
• Total Countries  
• Total Population

These provide a **quick overview of global inequality metrics**.

---

### 3. Distribution Charts

These charts show how countries are distributed across
income groups and inequality categories.

---

### 4. Regional Comparison Charts

These charts compare inequality across regions,
helping identify economic differences.

---

### 5. Trend Charts

Trend charts help analyze **how inequality changes over time**.

---

### 6. Interactive Features

You can interact with the dashboard by:

• Clicking charts to filter other visuals  
• Hovering to see detailed values  
• Using slicers to change the analysis scope

---

### 7. Insights Generation

By combining filters and charts,
users can generate **custom insights about global inequality patterns**.
""")

# --------------------------------
# FAQ
# --------------------------------

elif page == "FAQ":

    st.title("FAQ")

    with st.expander("What is the Gini Index?"):
        st.write("The Gini Index measures income inequality within a country.")

    with st.expander("What is Palma Ratio?"):
        st.write("Palma Ratio compares income share of richest 10% vs poorest 40%.")

    with st.expander("Why analyze inequality?"):
        st.write("It helps governments understand economic imbalance.")

# --------------------------------
# FEEDBACK
# --------------------------------

elif page == "Feedback":

    st.title("User Feedback")

    with st.form("feedback"):

        name = st.text_input("Name")
        rating = st.slider("Rating",1,5)
        comment = st.text_area("Comment")

        submit = st.form_submit_button("Submit")

        if submit:

            with open("feedback.txt","a") as f:
                f.write(f"{name},{rating},{comment},{datetime.now()}\n")

            st.success("Thank you for your feedback!")
