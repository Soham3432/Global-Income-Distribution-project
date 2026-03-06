import streamlit as st
import pandas as pd
from datetime import datetime
import os

# =================================
# PAGE CONFIG & THEME
# =================================
st.set_page_config(
    page_title="Nexus | Global Inequality Analytics",
    layout="wide",
    page_icon="🔮"
)

# Advanced Dark Purple Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: radial-gradient(circle at 20% 20%, #1e0a3d 0%, #09050f 100%);
        color: #e0d5ff;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(15, 5, 30, 0.9) !important;
        border-right: 1px solid rgba(188, 122, 255, 0.2);
    }

    /* Modern Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }

    /* Neon KPI Cards */
    .kpi-container {
        background: linear-gradient(135deg, rgba(108, 92, 231, 0.1), rgba(188, 122, 255, 0.05));
        border-radius: 24px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(188, 122, 255, 0.3);
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .kpi-container:hover {
        transform: translateY(-8px);
        border-color: #bc7aff;
        box-shadow: 0 0 25px rgba(188, 122, 255, 0.3);
    }

    .kpi-val {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #bc7aff, #6c5ce7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .kpi-lab {
        font-size: 0.85rem;
        color: #a29bfe;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# =================================
# NAVIGATION
# =================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="glass-card" style="width:400px; margin:150px auto; text-align:center;">', unsafe_allow_html=True)
    st.title("🔮 Nexus Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Enter Platform"):
        if u == "admin" and p == "1234":
            st.session_state.logged_in = True
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =================================
# DASHBOARD LOGIC (BASED ON PROJECT DATA)
# =================================
with st.sidebar:
    st.markdown("<h2 style='color:#bc7aff;'>NEXUS CORE</h2>", unsafe_allow_html=True)
    page = st.radio("SENSORS", ["Global Intelligence", "Neural Insights", "Data Pipeline", "User Feedback"])
    st.markdown("---")
    st.caption("User: Yash Chaudhari")

if page == "Global Intelligence":
    st.markdown("<h1>System <span style='color:#bc7aff'>Intelligence</span></h1>", unsafe_allow_html=True)
    
    # KPIs based on your specific project metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="kpi-container"><p class="kpi-val">41.2</p><p class="kpi-lab">Avg Gini Index</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="kpi-container"><p class="kpi-val">1.84</p><p class="kpi-lab">Palma Ratio</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="kpi-container"><p class="kpi-val">7.2x</p><p class="kpi-lab">20/20 Gap Ratio</p></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="kpi-container"><p class="kpi-val">0.48</p><p class="kpi-lab">Inequality Index</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Dashboard Integration
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Interactive Heatmap & Distribution")
    pbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"
    st.components.v1.iframe(pbi_url, height=700)
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "Neural Insights":
    st.title("📈 Strategic Findings")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <div class="glass-card">
        <h4>Income Quintile Breakdown</h4>
        <p>Analysis of Q1 (Poorest 20%) through Q5 (Richest 20%) shows a deepening concentration in high-income regions.</p>
        <ul style="color:#a29bfe;">
            <li><b>Bottom 40%:</b> Significant share reduction in Sub-Saharan Africa.</li>
            <li><b>Top 10%:</b> Capturing >50% of national income in 14 surveyed nations.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("""
        <div class="glass-card">
        <h4>Regional Disparity</h4>
        <p>World Bank data indicates that while global averages remain stable, the <b>Palma Ratio</b> is increasing in developing economies.</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "Data Pipeline":
    st.title("🏗 Architecture")
    st.markdown("""
    <div class="glass-card">
    <h4>Data Schema</h4>
    <p>Integrated sources: World Bank, UNDP Inequality Index, and Local Survey Data.</p>
    <code>
    Columns: [Country, Region, Gini_WB, Palma_Ratio, Q1_Share, Q5_Share, UNDP_Index]
    </code>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<p style='text-align:center; opacity:0.5;'>NEXUS ANALYTICS | v2.0-PURPLE</p>", unsafe_allow_html=True)
