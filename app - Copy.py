import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------

st.set_page_config(
    page_title="Global Income Distribution Analytics",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------------------------------
# ADVANCED UI STYLE
# -------------------------------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(-45deg,#0f0c29,#302b63,#24243e,#0f001f);
background-size:400% 400%;
animation:gradientBG 18s ease infinite;
color:white;
}

@keyframes gradientBG{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

section[data-testid="stSidebar"]{
background:rgba(20,0,40,0.9);
backdrop-filter:blur(10px);
}

.card{
background:rgba(255,255,255,0.08);
padding:25px;
border-radius:18px;
text-align:center;
font-weight:bold;
box-shadow:0 15px 35px rgba(0,0,0,0.6);
transition:all .3s ease;
}

.card:hover{
transform:translateY(-10px) scale(1.05);
box-shadow:0 20px 45px rgba(0,255,255,0.4);
}

.section{
background:rgba(255,255,255,0.05);
padding:30px;
border-radius:15px;
margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# LOGIN SYSTEM
# -------------------------------------------------------

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

# -------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------

st.sidebar.title("🌍 Analytics Platform")

page = st.sidebar.radio(
"Navigation",
[
"Executive Overview",
"Interactive Dashboard",
"Global Inequality Map",
"Country Comparison",
"Leaderboard",
"Country Explorer",
"Data Analytics",
"Charts Explanation",
"Dashboard Guide",
"FAQ",
"Feedback"
]
)

# -------------------------------------------------------
# EXECUTIVE OVERVIEW
# -------------------------------------------------------

if page == "Executive Overview":

    st.title("Global Income Distribution Analytics")

    st.markdown("""
This platform analyzes **global income inequality** using economic indicators
like **Gini Index, Palma Ratio, and Income Distribution Metrics**.
""")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.markdown('<div class="card"><h3>62.49</h3>Inequality Range</div>',unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><h3>37.52</h3>Average Gini Index</div>',unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card"><h3>22.55</h3>Inequality Index</div>',unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card"><h3>200</h3>Total Countries</div>',unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="card"><h3>7.85B</h3>World Population</div>',unsafe_allow_html=True)

    st.subheader("Global Inequality Trend")

    years=[2016,2017,2018,2019,2020,2021,2022,2023]
    gini=[38,37.5,37.6,37.3,37.2,37.4,37.5,37.6]

    fig=px.line(x=years,y=gini,labels={"x":"Year","y":"Gini Index"})
    st.plotly_chart(fig,use_container_width=True)

    if st.button("Generate Insights"):

        st.markdown("""
### Automated Insights

• Global inequality remains high in developing regions  
• Latin America and Africa show higher Gini values  
• Developed countries tend to have lower inequality  
""")

# -------------------------------------------------------
# POWER BI DASHBOARD
# -------------------------------------------------------

elif page == "Interactive Dashboard":

    st.title("📊 Global Income Dashboard")

    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,width=1400,height=800)

# -------------------------------------------------------
# GLOBAL MAP
# -------------------------------------------------------

elif page == "Global Inequality Map":

    st.title("🌍 Global Inequality Map")

    data={
    "Country":["United States","India","Brazil","South Africa","Germany","Japan"],
    "ISO":["USA","IND","BRA","ZAF","DEU","JPN"],
    "Gini":[41,35,53,63,31,32]
    }

    df=pd.DataFrame(data)

    fig=px.choropleth(
        df,
        locations="ISO",
        color="Gini",
        hover_name="Country",
        color_continuous_scale="reds"
    )

    st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# COUNTRY COMPARISON
# -------------------------------------------------------

elif page == "Country Comparison":

    st.title("📊 Country Comparison")

    countries=["USA","India","Brazil","Germany","Japan"]

    c1=st.selectbox("Country 1",countries)
    c2=st.selectbox("Country 2",countries,index=1)

    data={
    "Country":[c1,c2],
    "Gini":[41,35]
    }

    df=pd.DataFrame(data)

    fig=px.bar(df,x="Country",y="Gini",color="Country")
    st.plotly_chart(fig)

# -------------------------------------------------------
# LEADERBOARD
# -------------------------------------------------------

elif page=="Leaderboard":

    st.title("🏆 Global Inequality Leaderboard")

    data={
    "Country":["South Africa","Brazil","Colombia","Panama","Chile"],
    "Gini":[63,53,52,51,50]
    }

    df=pd.DataFrame(data)

    st.table(df)

    fig=px.bar(df,x="Country",y="Gini",color="Country")
    st.plotly_chart(fig)

# -------------------------------------------------------
# COUNTRY EXPLORER
# -------------------------------------------------------

elif page=="Country Explorer":

    st.title("🌍 Country Explorer")

    country=st.selectbox(
    "Select Country",
    ["USA","India","Brazil","Germany","Japan"]
    )

    if country=="USA":
        st.write("Gini Index: 41")

    elif country=="India":
        st.write("Gini Index: 35")

    elif country=="Brazil":
        st.write("Gini Index: 53")

# -------------------------------------------------------
# DATA ANALYTICS
# -------------------------------------------------------

elif page=="Data Analytics":

    st.title("📊 Dataset Analytics")

    data={
    "Country":["USA","India","Brazil","Germany","Japan"],
    "Gini":[41,35,53,31,32],
    "GDP":[70000,2400,9000,52000,41000]
    }

    df=pd.DataFrame(data)

    st.dataframe(df)

    st.write(df.describe())

    fig=px.scatter(df,x="GDP",y="Gini",text="Country")
    st.plotly_chart(fig)

# -------------------------------------------------------
# CHART EXPLANATION
# -------------------------------------------------------

elif page=="Charts Explanation":

    st.title("Chart Explanation")

    st.write("""
Charts explain global inequality trends, income distribution,
and country comparisons using economic indicators.
""")

# -------------------------------------------------------
# DASHBOARD GUIDE
# -------------------------------------------------------

elif page=="Dashboard Guide":

    st.title("Dashboard Guide")

    st.write("""
1. Use filters to select regions or income groups  
2. Explore charts for insights  
3. Compare countries for analysis  
""")

# -------------------------------------------------------
# FAQ
# -------------------------------------------------------

elif page=="FAQ":

    st.title("FAQ")

    with st.expander("What is Gini Index?"):
        st.write("A measure of income inequality.")

    with st.expander("What is Palma Ratio?"):
        st.write("Richest 10% vs poorest 40% income share.")

# -------------------------------------------------------
# FEEDBACK
# -------------------------------------------------------

elif page=="Feedback":

    st.title("User Feedback")

    with st.form("feedback"):

        name=st.text_input("Name")
        rating=st.slider("Rating",1,5)
        comment=st.text_area("Comment")

        submit=st.form_submit_button("Submit")

        if submit:

            with open("feedback.txt","a") as f:
                f.write(f"{name},{rating},{comment},{datetime.now()}\n")

            st.success("Feedback submitted")
