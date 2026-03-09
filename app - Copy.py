import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Global Income Distribution Intelligence Platform", layout="wide")

# ------------------ UI STYLE ------------------ #

st.markdown("""
<style>

body {
background: linear-gradient(135deg,#0f0033,#1c004d);
color:white;
}

.glass {
background: rgba(255,255,255,0.05);
border-radius:16px;
padding:25px;
backdrop-filter: blur(10px);
box-shadow:0px 8px 30px rgba(0,0,0,0.6);
}

.title {
font-size:48px;
text-align:center;
font-weight:700;
color:#cdb7ff;
}

.metric {
font-size:30px;
font-weight:bold;
color:#9f8bff;
}

.sidebar .sidebar-content {
background:#150a3d;
}

</style>
""", unsafe_allow_html=True)

# ------------------ SAMPLE DATA ------------------ #

countries = ["USA","India","Brazil","Germany","China","South Africa","UK","France","Japan","Canada"]
iso = ["USA","IND","BRA","DEU","CHN","ZAF","GBR","FRA","JPN","CAN"]
gini = [41,35,53,31,38,63,34,32,33,30]
years = [2000,2005,2010,2015,2020]

trend_data = {
"USA":[38,39,40,41,42],
"India":[30,32,33,34,35],
"Brazil":[55,54,53,52,53],
"Germany":[29,30,30,31,31],
"China":[35,36,37,38,38]
}

# ------------------ LOGIN ------------------ #

if "logged" not in st.session_state:
    st.session_state.logged=False

if not st.session_state.logged:

    st.markdown("<div class='title'>Global Income Distribution Intelligence Platform</div>",unsafe_allow_html=True)

    st.write("")
    st.write("")

    user=st.text_input("Username")
    pw=st.text_input("Password",type="password")

    if st.button("Login"):
        if user=="admin" and pw=="1234":
            st.session_state.logged=True
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# ------------------ SIDEBAR ------------------ #

menu=st.sidebar.selectbox("Navigation",[
"Executive Dashboard",
"Power BI Dashboard",
"Global Inequality Map",
"Inequality Trends",
"Country Comparison",
"Income Distribution",
"Inequality Simulator",
"Prediction Model",
"AI Insights",
"Data Story",
"Policy Intelligence",
"Quiz",
"FAQ",
"Dashboard Guide",
"About Project"
])

# ------------------ EXECUTIVE DASHBOARD ------------------ #

if menu=="Executive Dashboard":

    st.markdown("<div class='title'>Global Inequality Executive Dashboard</div>",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.markdown("<div class='glass'>Average Global Gini<div class='metric'>38.5</div></div>",unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='glass'>Highest Inequality<div class='metric'>South Africa</div></div>",unsafe_allow_html=True)

    with c3:
        st.markdown("<div class='glass'>Lowest Inequality<div class='metric'>Canada</div></div>",unsafe_allow_html=True)

    with c4:
        st.markdown("<div class='glass'>Countries Analyzed<div class='metric'>100+</div></div>",unsafe_allow_html=True)

    fig=px.bar(x=countries,y=gini,title="Global Inequality Comparison")
    st.plotly_chart(fig,use_container_width=True)

# ------------------ POWER BI EMBED ------------------ #

elif menu=="Power BI Dashboard":

    st.title("Power BI Analytics Dashboard")

    st.write("Embedded Power BI dashboard below.")

    powerbi_url=("https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9")
        st.components.v1.iframe(powerbi_url,height=700)

    st.info("Get embed link from Power BI → File → Embed → Website")

# ------------------ GLOBAL MAP ------------------ #

elif menu=="Global Inequality Map":

    st.title("Global Inequality Map")

    fig=px.choropleth(
    locations=iso,
    color=gini,
    hover_name=countries,
    color_continuous_scale="Plasma"
    )

    st.plotly_chart(fig,use_container_width=True)

# ------------------ TRENDS ------------------ #

elif menu=="Inequality Trends":

    st.title("Income Inequality Trends")

    country=st.selectbox("Select Country",list(trend_data.keys()))

    fig=px.line(x=years,y=trend_data[country],title=f"{country} Inequality Trend")
    st.plotly_chart(fig,use_container_width=True)

# ------------------ COUNTRY COMPARISON ------------------ #

elif menu=="Country Comparison":

    st.title("Country Comparison Tool")

    c1=st.selectbox("Country 1",countries)
    c2=st.selectbox("Country 2",countries)

    g1=gini[countries.index(c1)]
    g2=gini[countries.index(c2)]

    fig=go.Figure()

    fig.add_bar(name=c1,x=["Gini"],y=[g1])
    fig.add_bar(name=c2,x=["Gini"],y=[g2])

    st.plotly_chart(fig,use_container_width=True)

# ------------------ INCOME SHARE ------------------ #

elif menu=="Income Distribution":

    groups=["Top 10%","Middle 40%","Bottom 50%"]
    share=[52,35,13]

    fig=px.pie(values=share,names=groups,title="Global Income Distribution")
    st.plotly_chart(fig,use_container_width=True)

# ------------------ SIMULATOR ------------------ #

elif menu=="Inequality Simulator":

    st.title("Policy Impact Simulator")

    tax=st.slider("Tax Rate",0,60,20)
    welfare=st.slider("Welfare Spending",0,50,15)

    base=45

    new=base-(tax*0.2)-(welfare*0.1)

    st.metric("Estimated Gini Index",round(new,2))

# ------------------ PREDICTION ------------------ #

elif menu=="Prediction Model":

    st.title("Inequality Prediction Model")

    gdp=st.slider("GDP per Capita",1000,80000,20000)
    education=st.slider("Education Index",0.1,1.0,0.6)

    predicted=50-(gdp/10000)-(education*10)

    st.metric("Predicted Gini Index",round(predicted,2))

# ------------------ AI INSIGHTS ------------------ #

elif menu=="AI Insights":

    st.title("AI Generated Insights")

    insights=[
    "Countries with strong welfare systems show lower inequality.",
    "High GDP does not always mean equal income distribution.",
    "Education access strongly correlates with equality.",
    "Progressive taxation helps reduce income concentration."
    ]

    st.success(random.choice(insights))

# ------------------ STORY ------------------ #

elif menu=="Data Story":

    step=st.slider("Story Step",1,4)

    if step==1:
        st.write("Global inequality has grown since the 1980s.")

    if step==2:
        st.write("Technological growth increased wealth concentration.")

    if step==3:
        st.write("Policy interventions help balance income.")

    if step==4:
        st.write("Future reforms could reshape economic distribution.")

# ------------------ POLICY ------------------ #

elif menu=="Policy Intelligence":

    st.title("Policy Solutions")

    st.markdown("""
### Progressive Taxation  
Redistributes wealth through higher tax brackets.

### Education Investment  
Improves economic mobility.

### Universal Healthcare  
Prevents poverty traps.

### Social Protection Programs  
Protect vulnerable populations.
""")

# ------------------ QUIZ ------------------ #

elif menu=="Quiz":

    st.title("Inequality Knowledge Quiz")

    q=st.radio("What does Gini = 0 represent?",
    ["Perfect Equality","Perfect Inequality","Economic Growth"])

    if st.button("Submit"):

        if q=="Perfect Equality":
            st.success("Correct!")
        else:
            st.error("Incorrect")

# ------------------ FAQ ------------------ #

elif menu=="FAQ":

    with st.expander("What is income inequality?"):
        st.write("Unequal distribution of income among population.")

    with st.expander("What is Gini index?"):
        st.write("Measurement of inequality from 0 to 100.")

# ------------------ GUIDE ------------------ #

elif menu=="Dashboard Guide":

    st.write("""
This platform allows exploration of global inequality through:

• Interactive maps  
• Trend analysis  
• Country comparison  
• Policy simulations  
• AI insights  
• Embedded Power BI dashboards
""")

# ------------------ ABOUT ------------------ #

elif menu=="About Project":

    st.write("""
Global Income Distribution Intelligence Platform

Tools Used:
• Streamlit
• Plotly
• Power BI

Purpose:
To analyze global income inequality through interactive analytics.
""")


