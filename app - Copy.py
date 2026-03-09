import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Income Distribution Dashboard",
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
animation:gradientBG 15s ease infinite;
color:white;
}

@keyframes gradientBG{
0%{background-position:0% 50%;}
50%{background-position:100% 50%;}
100%{background-position:0% 50%;}
}

[data-testid="stSidebar"]{
background:rgba(15,0,40,0.9);
backdrop-filter:blur(10px);
}

.metric-card{
background:rgba(255,255,255,0.05);
border-radius:18px;
padding:25px;
text-align:center;
border:1px solid rgba(255,255,255,0.1);
transition:0.3s;
}

.metric-card:hover{
transform:scale(1.05);
box-shadow:0 10px 30px rgba(0,255,255,0.3);
}

.metric-value{
font-size:32px;
font-weight:bold;
background:linear-gradient(90deg,#00f2fe,#4facfe);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.metric-label{
font-size:14px;
color:#ccc;
}

.section-card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:15px;
border:1px solid rgba(255,255,255,0.1);
margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# LOGIN SYSTEM
# -------------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:

    st.title("🌍 Global Income Distribution Dashboard")

    st.write("### Login to Explore Global Inequality Insights")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

df = pd.read_csv("income_data.csv")

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Charts",
        "Dataset",
        "Dashboard Guide",
        "FAQ",
        "Feedback"
    ]
)

# -------------------------------------------------------
# DASHBOARD PAGE
# -------------------------------------------------------

if page == "Dashboard":

    st.title("🌍 Global Income Inequality Overview")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">200</div>
        <div class="metric-label">Total Countries</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">37.52</div>
        <div class="metric-label">Avg Gini Index</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">22.55</div>
        <div class="metric-label">Avg Inequality Index</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">62.49</div>
        <div class="metric-label">Inequality Range</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-value">7.8B</div>
        <div class="metric-label">World Population</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Income Group Distribution")

    fig = px.histogram(
        df,
        x="Income_Group",
        color="Income_Group"
    )

    st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# CHARTS PAGE
# -------------------------------------------------------

elif page == "Charts":

    st.title("📊 Inequality Charts")

    chart = st.selectbox(
        "Select Chart",
        [
            "Richest 20% Income Share",
            "Gini Index by Country",
            "Top 10 Inequality Countries"
        ]
    )

    if chart == "Richest 20% Income Share":

        fig = px.bar(
            df.head(20),
            x="Country",
            y="Richest_20_Share",
            color="Income_Group"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart == "Gini Index by Country":

        fig = px.scatter(
            df,
            x="GDP_per_capita",
            y="Gini_Index",
            color="Income_Group",
            hover_name="Country"
        )

        st.plotly_chart(fig,use_container_width=True)

    elif chart == "Top 10 Inequality Countries":

        top = df.sort_values("Gini_Index",ascending=False).head(10)

        fig = px.bar(
            top,
            x="Country",
            y="Gini_Index",
            color="Country"
        )

        st.plotly_chart(fig,use_container_width=True)

# -------------------------------------------------------
# DATASET PAGE
# -------------------------------------------------------

elif page == "Dataset":

    st.title("📂 Dataset Preview")

    st.write("Explore the dataset used in this project.")

    st.dataframe(df)

# -------------------------------------------------------
# DASHBOARD GUIDE
# -------------------------------------------------------

elif page == "Dashboard Guide":

    st.title("📘 Dashboard Guide")

    with st.expander("What is Gini Index?"):
        st.write("""
The Gini Index measures income inequality within a population.

0 = perfect equality  
100 = maximum inequality
""")

    with st.expander("What is Palma Ratio?"):
        st.write("""
The Palma Ratio compares income of the richest 10%
to the poorest 40%.
""")

    with st.expander("How to use the dashboard?"):
        st.write("""
1. Use sidebar navigation  
2. Explore charts  
3. Compare countries  
4. Analyze inequality trends
""")

# -------------------------------------------------------
# FAQ
# -------------------------------------------------------

elif page == "FAQ":

    st.title("❓ Frequently Asked Questions")

    with st.expander("What data source is used?"):
        st.write("World Bank Global Income dataset.")

    with st.expander("What does inequality mean?"):
        st.write("Unequal distribution of income among population.")

    with st.expander("How often is data updated?"):
        st.write("Depends on World Bank updates.")

# -------------------------------------------------------
# FEEDBACK
# -------------------------------------------------------

elif page == "Feedback":

    st.title("💬 Feedback")

    name = st.text_input("Your Name")
    email = st.text_input("Email")
    feedback = st.text_area("Your Feedback")

    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
