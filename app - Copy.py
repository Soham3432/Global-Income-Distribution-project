import streamlit as st
from datetime import datetime
import os

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Global Income Distribution Analytics",
    layout="wide",
    page_icon="🌍"
)

# ==============================
# DARK PURPLE UI
# ==============================

st.markdown("""
<style>

body{
background:linear-gradient(135deg,#12001f,#2a004f,#4b0082);
color:white;
}

.stApp{
background:linear-gradient(135deg,#12001f,#2a004f,#4b0082);
}

section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#1b0033,#3a0066);
}

.card{
background:linear-gradient(145deg,#6a11cb,#2575fc);
padding:25px;
border-radius:15px;
text-align:center;
font-weight:bold;
box-shadow:0px 8px 30px rgba(0,0,0,0.6);
margin-bottom:15px;
}

.section{
background:rgba(255,255,255,0.05);
backdrop-filter:blur(12px);
padding:30px;
border-radius:15px;
box-shadow:0px 10px 40px rgba(0,0,0,0.7);
margin-bottom:25px;
}

h1{
text-shadow:0px 0px 15px #d000ff;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# LOGIN SYSTEM
# ==============================

def login():

    st.title("🌍 Global Income Distribution Analytics Platform")

    st.markdown("### Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "1234":

            st.session_state.logged = True
            st.success("Login Successful")

        else:

            st.error("Invalid credentials")


if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    login()
    st.stop()

# ==============================
# SIDEBAR NAVIGATION
# ==============================

st.sidebar.title("🌍 Analytics Platform")

page = st.sidebar.radio(
"Navigation",
[
"Executive Overview",
"Dashboard",
"Chart Explorer",
"Dashboard Guide",
"FAQ",
"Feedback"
]
)

# ==============================
# EXECUTIVE OVERVIEW
# ==============================

if page == "Executive Overview":

    st.title("Global Income Distribution Analytics")

    st.markdown('<div class="section">This platform analyzes global income inequality trends using interactive data visualizations.</div>', unsafe_allow_html=True)

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.markdown('<div class="card"><h3>62.49</h3>Inequality Range</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><h3>37.52</h3>Avg Gini Index</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card"><h3>22.55</h3>Avg Inequality Index</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card"><h3>200</h3>Total Countries</div>', unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="card"><h3>7.85B</h3>Total Updated Population</div>', unsafe_allow_html=True)

# ==============================
# DASHBOARD
# ==============================

elif page == "Dashboard":

    st.title("📊 Interactive Dashboard")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,width=1400,height=750)

# ==============================
# CHART EXPLORER
# ==============================

elif page == "Chart Explorer":

    st.title("📊 Chart Explorer")

    chart = st.selectbox(
    "Select Chart",
    [
    "Country Distribution by Income Group",
    "Richest 20% Income Share by Region",
    "Palma Ratio by World Bank Group",
    "Top 5 Countries by Inequality",
    "Global Gini Index Trend",
    "Categories by Inequality Level"
    ])

    if chart == "Country Distribution by Income Group":

        st.markdown("""
        **Purpose**

        Shows how countries are distributed across income categories.

        **Insights**

        - High income countries represent developed economies.
        - Lower income groups show emerging or developing economies.
        """)

    elif chart == "Richest 20% Income Share by Region":

        st.markdown("""
        **Purpose**

        Shows how much income the richest 20% control in each region.

        **Insight**

        Regions with higher values indicate stronger wealth concentration.
        """)

    elif chart == "Palma Ratio by World Bank Group":

        st.markdown("""
        **Purpose**

        Palma Ratio compares the richest 10% income to the poorest 40%.

        **Insight**

        Higher ratio = greater inequality.
        """)

    elif chart == "Top 5 Countries by Inequality":

        st.markdown("""
        **Purpose**

        Identifies countries with the highest income inequality.

        **Insight**

        These countries require economic policy interventions.
        """)

    elif chart == "Global Gini Index Trend":

        st.markdown("""
        **Purpose**

        Shows inequality trend across decades.

        **Insight**

        Helps analyze how global inequality evolved historically.
        """)

    elif chart == "Categories by Inequality Level":

        st.markdown("""
        **Purpose**

        Groups countries into inequality levels.

        **Insight**

        Medium inequality category contains most countries.
        """)

# ==============================
# DASHBOARD GUIDE
# ==============================

elif page == "Dashboard Guide":

    st.title("📘 Dashboard Guide")

    st.markdown("""
    **How to Use the Dashboard**

    1. Use filters at the top to select region or year.
    2. Hover over charts to see detailed values.
    3. Click charts to filter other visuals.
    4. Compare regions using bar charts.
    5. Track historical inequality using the trend chart.

    **Main Metrics**

    • Gini Index – inequality indicator  
    • Palma Ratio – wealth distribution measure  
    • Income Share – income concentration  
    """)

# ==============================
# FAQ
# ==============================

elif page == "FAQ":

    st.title("FAQ")

    with st.expander("What is Gini Index?"):
        st.write("The Gini Index measures income inequality.")

    with st.expander("What is Palma Ratio?"):
        st.write("Palma ratio compares richest 10% to poorest 40% income share.")

    with st.expander("Why analyze income inequality?"):
        st.write("It helps policymakers understand economic disparities.")

# ==============================
# FEEDBACK
# ==============================

elif page == "Feedback":

    st.title("Feedback")

    with st.form("feedback"):

        name = st.text_input("Name")
        rating = st.slider("Rating",1,5)
        comment = st.text_area("Comments")

        submit = st.form_submit_button("Submit")

        if submit:

            data = f"{name},{rating},{comment},{datetime.now()}\n"

            with open("feedback.txt","a") as f:
                f.write(data)

            st.success("Thank you for your feedback!")

# ==============================
# FOOTER
# ==============================

st.markdown("""
---
Global Income Distribution Analytics Platform  
Built using Power BI + Streamlit
""")
