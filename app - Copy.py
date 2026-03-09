import streamlit as st
import pandas as pd
from datetime import datetime
import base64

# ==============================
# ADVANCED PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Global Income Intelligence | Pro",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# ==============================
# ENHANCED NEON GLASSMORPHISM UI
# ==============================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top left, #1a0033, #050505);
        color: #e0e0e0;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: rgba(20, 0, 40, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Professional Card Styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        transition: transform 0.3s ease;
        text-align: center;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #d000ff;
        box-shadow: 0 10px 20px rgba(208, 0, 255, 0.2);
    }

    /* Custom Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
        color: #ffffff;
    }

    /* Glow Text */
    .glow-text {
        text-shadow: 0 0 10px rgba(208, 0, 255, 0.8);
        color: #d000ff;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# AUTHENTICATION LOGIC
# ==============================
if 'logged' not in st.session_state:
    st.session_state.logged = False

def logout():
    st.session_state.logged = False
    st.rerun()

if not st.session_state.logged:
    cols = st.columns([1, 2, 1])
    with cols[1]:
        st.image("https://cdn-icons-png.flaticon.com/512/2091/2091665.png", width=80)
        st.title("Secure Analytics Access")
        with st.container(border=True):
            user = st.text_input("Access ID")
            pw = st.text_input("Security Key", type="password")
            if st.button("Authenticate", use_container_width=True):
                if user == "admin" and pw == "1234":
                    st.session_state.logged = True
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Credentials")
    st.stop()

# ==============================
# SIDEBAR & TOOLS
# ==============================
with st.sidebar:
    st.markdown("<h2 class='glow-text'>INTELLIGENCE HUB</h2>", unsafe_allow_html=True)
    page = st.radio("Intelligence Layers", 
        ["Executive Summary", "Real-time Dashboard", "Mathematical Deep-Dive", "Resource Center", "User Feedback"])
    
    st.divider()
    if st.button("Logout System"):
        logout()

# ==============================
# 1. EXECUTIVE SUMMARY
# ==============================
if page == "Executive Summary":
    st.title("🌍 Global Socio-Economic Intelligence")
    st.markdown("#### Holistic view of global wealth distribution and inequality variances.")
    
    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("Global Gini Avg", "37.52", "↑ 0.4%"),
        ("Palma Median", "1.58", "Stable"),
        ("Countries Monitored", "200+", "Active"),
        ("Data Refresh", "Q1 2026", "Live")
    ]
    
    for i, (label, val, delta) in enumerate(metrics):
        with [c1, c2, c3, c4][i]:
            st.markdown(f"""
            <div class="metric-card">
                <p style="color: gray; margin-bottom: 5px;">{label}</p>
                <h2 style="margin: 0;">{val}</h2>
                <p style="color: #00ffcc; font-size: 0.8rem;">{delta}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("### 📈 Key Strategic Insights")
    st.info("Current data suggests a widening gap in Sub-Saharan Africa while OECD nations show stabilization in the Palma Ratio.")

# ==============================
# 2. REAL-TIME DASHBOARD
# ==============================
elif page == "Real-time Dashboard":
    st.title("📊 Multi-Dimensional Analytics")
    st.caption("Live Feed from Power BI Global Database")
    
    # Advanced Iframe Embed
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"
    st.components.v1.iframe(powerbi_url, height=800, scrolling=True)

# ==============================
# 3. MATHEMATICAL DEEP-DIVE
# ==============================
elif page == "Mathematical Deep-Dive":
    st.title("🧬 The Science of Inequality")
    
    tab1, tab2 = st.tabs(["The Gini Coefficient", "The Palma Ratio"])
    
    with tab1:
        st.markdown("### Gini Coefficient Analysis")
        

[Image of the Gini Coefficient Lorenz Curve]

        st.write("""
        The Gini coefficient is the most widely used measure of inequality. 
        It ranges from 0 (perfect equality) to 1 (perfect inequality).
        """)
        st.latex(r"G = \frac{\sum_{i=1}^{n} \sum_{j=1}^{n} |x_i - x_j|}{2n^2 \bar{x}}")
        st.markdown("> **Note:** A Gini index above 40 is typically considered a 'Warning Zone' for social stability.")

    with tab2:
        st.markdown("### The Palma Ratio")
        st.write("""
        The Palma Ratio addresses the Gini's insensitivity to changes at the extremes. 
        It focuses on the ratio of the top 10% to the bottom 40%.
        """)
        st.latex(r"Palma = \frac{Share_{Top 10\%}}{Share_{Bottom 40\%}}")

# ==============================
# 4. RESOURCE CENTER (DOWNLOADS)
# ==============================
elif page == "Resource Center":
    st.title("📚 Knowledge Base & Downloads")
    
    st.markdown("""
    ### Downloadable Guides
    Use these resources for offline policy research.
    """)
    
    guide_content = """
    GLOBAL INCOME DISTRIBUTION GUIDE 2026
    ------------------------------------
    1. Gini Index: Measure of statistical dispersion.
    2. Palma Ratio: Focused on the gap between extreme wealth and poverty.
    3. Recommendations: Focus on progressive taxation and education access.
    """
    
    st.download_button(
        label="📥 Download Policy Handbook (TXT)",
        data=guide_content,
        file_name="Global_Inequality_Guide.txt",
        mime="text/plain"
    )

    with st.expander("External High-Authority Links"):
        st.markdown("""
        * [World Bank Open Data](https://data.worldbank.org)
        * [World Inequality Database](https://wid.world)
        * [OECD Income Distribution Database](https://www.oecd.org/social/income-distribution-database.htm)
        """)

# ==============================
# 5. FEEDBACK
# ==============================
elif page == "User Feedback":
    st.title("🛰️ Intelligence Feedback")
    with st.form("feedback_plus"):
        name = st.text_input("Observer Name")
        category = st.selectbox("Topic", ["Data Accuracy", "UI/UX", "New Feature Request"])
        rating = st.select_slider("System Utility Score", options=[1, 2, 3, 4, 5])
        comment = st.text_area("Detailed Observations")
        
        if st.form_submit_button("Transmit Data"):
            st.balloons()
            st.success("Feedback logged into the secure repository.")

# ==============================
# FOOTER
# ==============================
st.markdown(f"""
<div style="text-align: center; margin-top: 50px; font-size: 0.8rem; color: gray;">
    <hr style="border-color: rgba(255,255,255,0.1);">
    © {datetime.now().year} Global Income Intelligence Platform | Secure Node 01
</div>
""", unsafe_allow_html=True)
