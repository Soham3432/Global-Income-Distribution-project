import streamlit as st
from datetime import datetime

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Global Income Analytics Pro",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------
# ADVANCED 3D LIVE UI CSS
# --------------------------------
st.markdown("""
<style>
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f001f);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Glassmorphic Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(20, 0, 40, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* 3D Glass Card Effect */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.5);
        box-shadow: 0 15px 40px rgba(0, 255, 255, 0.2);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #cbd5e0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Modernizing Buttons */
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(106, 17, 203, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOGIN LOGIC (Keep your existing logic here)
# --------------------------------
if "logged" not in st.session_state:
    st.session_state.logged = False

def login():
    st.markdown("<h1 style='text-align: center;'>Portal Login</h1>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Unlock Dashboard"):
                if username == "admin" and password == "1234":
                    st.session_state.logged = True
                    st.rerun()
                else:
                    st.error("Access Denied")

if not st.session_state.logged:
    login()
    st.stop()

# --------------------------------
# SIDEBAR & NAVIGATION
# --------------------------------
st.sidebar.title("🌍 Global Insights")
page = st.sidebar.radio("Navigation", ["Executive Overview", "Interactive Dashboard", "Charts Explanation", "FAQ"])

# --------------------------------
# UPDATED EXECUTIVE OVERVIEW
# --------------------------------
if page == "Executive Overview":
    st.title("🚀 Intelligence Overview")
    
    # 3D Metric Cards Row
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    
    metrics = [
        ("62.49", "Inequality Range"),
        ("37.52", "Avg Gini Index"),
        ("22.55", "Inequality Index"),
        ("200", "Total Countries"),
        ("7.85B", "Global Population")
    ]
    
    cols = [m_col1, m_col2, m_col3, m_col4, m_col5]
    
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metrics[i][0]}</div>
                    <div class="metric-label">{metrics[i][1]}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Using a 2-column layout for the intro
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("The Mission")
        st.info("This platform leverages real-time economic indicators to visualize the widening gap in global wealth distribution.")
        st.write("We track the **Gini Index** and **Palma Ratio** to provide actionable intelligence for policy makers.")
    
    with c2:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px;">
            <h4>Quick Links</h4>
            <li>View Regional Data</li>
            <li>Download Reports</li>
            <li>API Documentation</li>
        </div>
        """, unsafe_allow_html=True)

# (Keep your other 'elif' pages as they were, they will inherit the new background!)
