import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Global Income Distribution Dashboard", layout="wide")

# ---------------- UI STYLE ---------------- #

st.markdown("""
<style>

body{
background-color:#0E0033;
color:white;
}

.title{
text-align:center;
font-size:50px;
font-weight:bold;
color:#c9b6ff;
}

.card{
background:#1A0F4D;
padding:25px;
border-radius:15px;
text-align:center;
box-shadow:0px 5px 15px rgba(0,0,0,0.5);
}

.metric{
font-size:30px;
font-weight:bold;
color:#9f8bff;
}

.sidebar .sidebar-content{
background:#140a3d;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN PAGE ---------------- #

if "logged" not in st.session_state:
    st.session_state.logged=False

if not st.session_state.logged:

    st.markdown("<div class='title'>Global Income Distribution Dashboard</div>",unsafe_allow_html=True)

    st.write("")
    st.write("")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username=="admin" and password=="1234":
            st.session_state.logged=True
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# ---------------- SIDEBAR ---------------- #

menu = st.sidebar.selectbox(
"Navigation",
[
"Dashboard",
"Global Map",
"Country Comparison",
"Income Distribution",
"Inequality Simulator",
"Data Story Mode",
"Policy Insights",
"Quiz",
"FAQ",
"Dashboard Guide",
"About Project"
]
)

# ---------------- DASHBOARD ---------------- #

if menu=="Dashboard":

    st.markdown("<div class='title'>Global Inequality Overview</div>",unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown("""
        <div class="card">
        Average Global Gini
        <div class="metric">38.5</div>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        Highest Inequality Country
        <div class="metric">South Africa</div>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        Lowest Inequality Country
        <div class="metric">Slovenia</div>
        </div>
        """,unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="card">
        Countries Analyzed
        <div class="metric">120+</div>
        </div>
        """,unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Chart
    countries=["USA","India","Brazil","Germany","China","South Africa","UK"]
    gini=[41,35,53,31,38,63,34]

    fig=px.bar(x=countries,y=gini,title="Sample Global Inequality Comparison")
    st.plotly_chart(fig,use_container_width=True)

    with st.expander("Chart Explanation"):
        st.write("""
This chart shows **income inequality levels across countries**.

Higher Gini index values indicate **greater inequality**.

South Africa shows extremely high inequality compared to European countries like Germany.
""")

# ---------------- GLOBAL MAP ---------------- #

elif menu=="Global Map":

    st.title("Global Inequality Map")

    countries=["USA","India","Brazil","Germany","China","South Africa","UK"]
    iso=["USA","IND","BRA","DEU","CHN","ZAF","GBR"]
    gini=[41,35,53,31,38,63,34]

    fig=px.choropleth(
    locations=iso,
    color=gini,
    hover_name=countries,
    color_continuous_scale="Plasma",
    title="Global Income Inequality Map"
    )

    st.plotly_chart(fig,use_container_width=True)

    st.info("Darker colors represent higher inequality levels.")

# ---------------- COUNTRY COMPARISON ---------------- #

elif menu=="Country Comparison":

    st.title("Country Comparison Tool")

    countries=["USA","India","Brazil","Germany","China","South Africa","UK"]
    gini=[41,35,53,31,38,63,34]

    c1=st.selectbox("Select Country 1",countries)
    c2=st.selectbox("Select Country 2",countries)

    if st.button("Compare"):

        g1=gini[countries.index(c1)]
        g2=gini[countries.index(c2)]

        fig=go.Figure(data=[
        go.Bar(name=c1,x=["Gini"],y=[g1]),
        go.Bar(name=c2,x=["Gini"],y=[g2])
        ])

        st.plotly_chart(fig,use_container_width=True)

        st.write(f"{c1} Gini: {g1}")
        st.write(f"{c2} Gini: {g2}")

# ---------------- INCOME DISTRIBUTION ---------------- #

elif menu=="Income Distribution":

    st.title("Income Share Distribution")

    groups=["Top 10%","Middle 40%","Bottom 50%"]
    income=[52,35,13]

    fig=px.pie(values=income,names=groups,title="Global Income Share")

    st.plotly_chart(fig,use_container_width=True)

    with st.expander("Insight"):
        st.write("""
The top 10% controls over half of global income, 
while the bottom 50% receives a very small share.
""")

# ---------------- SIMULATOR ---------------- #

elif menu=="Inequality Simulator":

    st.title("Inequality Policy Simulator")

    tax=st.slider("Tax Rate (%)",0,60,20)
    welfare=st.slider("Social Welfare Spending (%)",0,50,15)

    base_gini=45

    new_gini=base_gini-(tax*0.2)-(welfare*0.1)

    st.metric("Estimated Gini Index",round(new_gini,2))

    st.info("Higher tax and welfare policies tend to reduce inequality.")

# ---------------- STORY MODE ---------------- #

elif menu=="Data Story Mode":

    st.title("Global Inequality Story")

    step=st.slider("Story Step",1,4)

    if step==1:
        st.write("Global inequality has increased significantly since 1980.")

    elif step==2:
        st.write("Emerging economies show rapid income growth but uneven distribution.")

    elif step==3:
        st.write("Policy intervention plays a major role in reducing inequality.")

    elif step==4:
        st.write("Future economic reforms may reshape income distribution.")

# ---------------- POLICY ---------------- #

elif menu=="Policy Insights":

    st.title("Policies That Reduce Inequality")

    st.markdown("""
### Progressive Taxation
Higher taxes on wealthy individuals redistribute income.

### Universal Education
Access to education increases income mobility.

### Healthcare Systems
Universal healthcare prevents poverty traps.

### Social Safety Nets
Government support reduces extreme poverty.
""")

# ---------------- QUIZ ---------------- #

elif menu=="Quiz":

    st.title("Income Inequality Quiz")

    q=st.radio(
    "What does Gini Index = 0 mean?",
    ["Perfect Equality","Perfect Inequality","Economic Growth"]
    )

    if st.button("Submit"):

        if q=="Perfect Equality":
            st.success("Correct!")
        else:
            st.error("Incorrect")

# ---------------- FAQ ---------------- #

elif menu=="FAQ":

    st.title("FAQ")

    with st.expander("What is Income Inequality?"):
        st.write("Income inequality refers to unequal income distribution across a population.")

    with st.expander("What is the Gini Index?"):
        st.write("The Gini index measures inequality from 0 (equal) to 100 (unequal).")

    with st.expander("Why does inequality matter?"):
        st.write("High inequality can reduce economic mobility and social stability.")

# ---------------- GUIDE ---------------- #

elif menu=="Dashboard Guide":

    st.title("Dashboard Guide")

    st.write("""
This dashboard helps users explore **global income inequality**.

Features included:

• Interactive charts  
• Global inequality map  
• Country comparison  
• Policy simulator  
• Educational insights  

Use the sidebar to explore different analytical tools.
""")

# ---------------- ABOUT ---------------- #

elif menu=="About Project":

    st.title("About This Project")

    st.write("""
**Global Income Distribution Dashboard**

This project demonstrates how data visualization can help analyze global economic inequality.

Tools Used:
- Streamlit
- Plotly

Goal:
To provide an interactive platform for exploring global income distribution patterns.
""")
