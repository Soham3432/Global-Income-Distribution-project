import streamlit as st
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Global Income Distribution Analytics",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# ADVANCED DARK PURPLE UI
# ---------------------------------------------------

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

# ---------------------------------------------------
# LOGIN SYSTEM
# ---------------------------------------------------

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

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------

st.sidebar.title("🌍 Analytics Platform")

page = st.sidebar.radio(
"Navigation",
[
"Executive Overview",
"Interactive Dashboard",
"Charts Explanation",
"Leaderboard",
"Country Explorer",
"Dashboard Guide",
"FAQ",
"Feedback"
]
)

# ---------------------------------------------------
# EXECUTIVE OVERVIEW
# ---------------------------------------------------

if page == "Executive Overview":

    st.title("Global Income Distribution Analytics")

    st.markdown("""
This platform analyzes **global income inequality and population distribution**  
using indicators such as **Gini Index, Palma Ratio, and Income Share**.

The project combines **data analytics, visualization, and economic insights**
to understand inequality trends worldwide.
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

    st.markdown("### Key Objectives")

    st.write("""
• Analyze global inequality trends  
• Identify countries with high inequality  
• Compare regions and income groups  
• Generate economic insights
""")

    if st.button("Generate Insights"):

        st.markdown("""
### Automated Insights

• Global inequality remains **high in developing regions**

• Latin America and Africa show **higher Gini values**

• Developed economies tend to show **lower inequality**

• Economic growth alone does not guarantee equality
""")

# ---------------------------------------------------
# INTERACTIVE DASHBOARD
# ---------------------------------------------------

elif page == "Interactive Dashboard":

    st.title("📊 Global Income Dashboard")

    st.markdown("""
The dashboard below provides an **interactive view of global income inequality**.

You can filter by:

• Income group  
• Region  
• Year  
• Country
""")

    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"

    st.components.v1.iframe(powerbi_url,width=1400,height=800)

# ---------------------------------------------------
# CHART EXPLANATIONS
# ---------------------------------------------------

elif page == "Charts Explanation":

    st.title("📊 Chart Explanations")

    chart = st.selectbox(
    "Select Chart",
    [
    "Income Group Distribution",
    "Richest 20% Income Share",
    "Palma Ratio",
    "Top Inequality Countries",
    "Global Gini Trend"
    ])

    if chart == "Income Group Distribution":

        st.write("""
Shows how countries are distributed across income groups:

• High income  
• Upper middle income  
• Lower middle income  
• Low income
""")

    elif chart == "Richest 20% Income Share":

        st.write("""
Shows the percentage of national income held by the **richest 20%**.
Higher percentages indicate stronger wealth concentration.
""")

    elif chart == "Palma Ratio":

        st.write("""
Palma Ratio compares the income share of the richest 10% with
the poorest 40% of the population.
""")

    elif chart == "Top Inequality Countries":

        st.write("""
This chart identifies countries with the **highest inequality levels globally**.
""")

    elif chart == "Global Gini Trend":

        st.write("""
Shows how global inequality levels have changed over time.
""")

# ---------------------------------------------------
# LEADERBOARD
# ---------------------------------------------------

elif page == "Leaderboard":

    st.title("🏆 Global Inequality Leaderboard")

    countries = [
    ("South Africa",63),
    ("Brazil",53),
    ("Colombia",52),
    ("Panama",51),
    ("Chile",50)
    ]

    for rank,(country,value) in enumerate(countries,start=1):

        st.markdown(f"""
        <div class="section">
        <h3>#{rank} {country}</h3>
        <p>Gini Index: {value}</p>
        </div>
        """,unsafe_allow_html=True)

# ---------------------------------------------------
# COUNTRY EXPLORER
# ---------------------------------------------------

elif page == "Country Explorer":

    st.title("🌍 Country Inequality Explorer")

    country = st.selectbox(
    "Select Country",
    [
    "United States",
    "India",
    "Brazil",
    "South Africa",
    "Germany",
    "Japan"
    ])

    if country == "United States":

        st.write("""
Gini Index: 41  
Income Group: High Income
""")

    elif country == "India":

        st.write("""
Gini Index: 35  
Income Group: Lower Middle Income
""")

    elif country == "Brazil":

        st.write("""
Gini Index: 53  
Income Group: Upper Middle Income
""")

    elif country == "South Africa":

        st.write("""
Gini Index: 63  
Income Group: Upper Middle Income
""")

    elif country == "Germany":

        st.write("""
Gini Index: 31  
Income Group: High Income
""")

    elif country == "Japan":

        st.write("""
Gini Index: 32  
Income Group: High Income
""")

# ---------------------------------------------------
# DASHBOARD GUIDE
# ---------------------------------------------------

elif page == "Dashboard Guide":

    st.title("📘 Dashboard Guide")

    st.write("""
### Filters
Use filters to analyze specific regions and income groups.

### KPI Cards
Provide summary metrics for global inequality.

### Charts
Visualize trends, comparisons, and distributions.

### Insights
Combine charts and filters to generate economic insights.
""")

# ---------------------------------------------------
# FAQ
# ---------------------------------------------------

elif page == "FAQ":

    st.title("Frequently Asked Questions")

    with st.expander("What is the Gini Index?"):
        st.write("The Gini Index measures inequality in income distribution.")

    with st.expander("What is Palma Ratio?"):
        st.write("Palma Ratio compares richest 10% income vs poorest 40%.")

    with st.expander("Why is inequality important?"):
        st.write("High inequality can impact economic growth and social stability.")

# ---------------------------------------------------
# FEEDBACK
# ---------------------------------------------------

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
