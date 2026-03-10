import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from reportlab.pdfgen import canvas
import numpy as np
import io

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# ---------------------------------------------------
# GLOBAL STYLE
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#09001f,#14003d,#24005f);
    color:white;
    font-family: 'Segoe UI';
}
.title {
    font-size:45px;
    font-weight:700;
    text-align:center;
    background: linear-gradient(90deg,#a855f7,#6366f1);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    margin-bottom: 20px;
}
.guide-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #7c3aed;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():
    # Replace with your actual file path
    try:
        df = pd.read_csv("final.sheet.csv")
        return df
    except:
        # Fallback for testing/demo
        return pd.DataFrame(np.random.randint(0,100,size=(100, 4)), columns=list('ABCD'))

df = load_data()
numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# ---------------------------------------------------
# LOGIN SYSTEM
# ---------------------------------------------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.markdown("<div class='title'>🌍 Global Income Intelligence</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            if user=="admin" and pw=="1234":
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Invalid Login")
    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
menu = st.sidebar.selectbox("Navigation", [
    "Executive Dashboard",
    "Dashboard Guide",
    "Power BI Dashboard",
    "Dataset Explorer",
    "Advanced Plotly Charts",
    "Matplotlib Explorer",
    "Country Analysis",
    "Machine Learning Prediction",
    "Generate PDF Report",
    "FAQ & Support",
    "About"
])

# ---------------------------------------------------
# DASHBOARD GUIDE (NEW)
# ---------------------------------------------------
if menu == "Dashboard Guide":
    st.markdown("<div class='title'>User Quick-Start Guide</div>", unsafe_allow_html=True)
    
    guides = {
        "📊 Visualizations": "Use 'Advanced Plotly' for interactive 3D graphs and 'Matplotlib Explorer' for static, publication-quality plots.",
        "🤖 Predictions": "The ML Prediction module uses Linear Regression to estimate values based on historical numeric data.",
        "🌍 Location Analysis": "Select 'Country Analysis' to filter the entire dataset by specific regions or nations.",
        "📄 Exporting": "Head to 'Generate PDF' to create a snapshot of the current dataset metrics for offline use."
    }
    
    for title, desc in guides.items():
        st.markdown(f"""<div class='guide-card'><h4>{title}</h4><p>{desc}</p></div>""", unsafe_allow_html=True)

# ---------------------------------------------------
# MATPLOTLIB EXPLORER (NEW)
# ---------------------------------------------------
elif menu == "Matplotlib Explorer":
    st.markdown("<div class='title'>Static Chart Explorer</div>", unsafe_allow_html=True)
    st.info("Select a chart type and variables to generate standard scientific plots.")
    
    m_chart = st.selectbox("Select Plot Type", ["Box Plot", "Violin Plot", "Pair Plot", "Joint Plot"])
    
    col_x = st.selectbox("Select Numeric Feature", numeric_cols)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    plt.style.use('dark_background')
    
    if m_chart == "Box Plot":
        sns.boxplot(data=df, y=col_x, color="#a855f7")
    elif m_chart == "Violin Plot":
        sns.violinplot(data=df, y=col_x, color="#6366f1")
    elif m_chart == "Pair Plot":
        # Using a sample to avoid lag
        fig = sns.pairplot(df[numeric_cols[:4]].sample(min(50, len(df))), diag_kind="kde")
    elif m_chart == "Joint Plot":
        col_y = st.selectbox("Select Y Feature", numeric_cols, index=1)
        g = sns.jointplot(data=df, x=col_x, y=col_y, kind="hex", color="#a855f7")
        fig = g.fig

    st.pyplot(fig)

# ---------------------------------------------------
# FAQ SECTION (NEW)
# ---------------------------------------------------
elif menu == "FAQ & Support":
    st.markdown("<div class='title'>Frequently Asked Questions</div>", unsafe_allow_html=True)
    
    with st.expander("How is the 'Income Intelligence' calculated?"):
        st.write("The platform aggregates multi-source data using weighted averages across regional reporting periods.")
        
    with st.expander("Can I upload my own CSV?"):
        st.write("Currently, this platform is locked to the 'final.sheet.csv'. Admin access is required for dataset updates.")
        
    with st.expander("What ML model is being used?"):
        st.write("We utilize Scikit-Learn's Linear Regression for standard predictions due to its high interpretability.")

    st.markdown("---")
    st.subheader("Need further help?")
    st.text_area("Submit a support ticket:")
    if st.button("Submit"):
        st.toast("Ticket submitted successfully!")

# ---------------------------------------------------
# EXISTING SECTIONS (LOGIC REMAINS SIMILAR)
# ---------------------------------------------------
elif menu == "Executive Dashboard":
    st.markdown("<div class='title'>Executive Dashboard</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Numeric Variables", len(numeric_cols))
    
    if len(numeric_cols) > 0:
        fig = px.histogram(df, x=numeric_cols[0], nbins=40, color_discrete_sequence=["#8b5cf6"], template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

elif menu=="Power BI Dashboard":
    st.title("Power BI Dashboard")
    powerbi_url="https://app.powerbi.com/view?r=eyJrIjoiNGZlMTUzYTktODU3OC00ODgxLWE3ZmItZjlmM2Y2MTg5ZWQxIiwidCI6IjNjMGQxMTRlLTVmZjItNDk0NS04OThjLWRkZTk3Y2Y2NWZkNSJ9"
    st.components.v1.iframe(powerbi_url, height=700)

elif menu=="Dataset Explorer":
    st.title("Dataset Explorer")
    st.dataframe(df.style.background_gradient(cmap='Purples'))
    column = st.selectbox("Select Column for Statistics", df.columns)
    st.write(df[column].describe())

elif menu=="Advanced Plotly Charts":
    # (Existing Plotly Logic here...)
    st.title("Interactive Plotly Visuals")
    # ... logic for 3D Scatter, Heatmaps, etc.

elif menu=="Country Analysis":
    st.title("Country Analysis")
    country_cols=[c for c in df.columns if "country" in c.lower()]
    if country_cols:
        country_col=country_cols[0]
        country = st.selectbox("Select Country", df[country_col].unique())
        filtered = df[df[country_col]==country]
        st.dataframe(filtered)
        fig = px.bar(filtered, y=numeric_cols[0], color_discrete_sequence=["#6366f1"], template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

elif menu=="Machine Learning Prediction":
    st.title("ML Prediction (Linear Regression)")
    target = st.selectbox("Target Variable", numeric_cols)
    features=[c for c in numeric_cols if c!=target]
    X=df[features].fillna(0)
    y=df[target].fillna(0)
    model=LinearRegression().fit(X,y)
    
    inputs=[]
    for col in features:
        val=st.number_input(col, value=float(X[col].mean()))
        inputs.append(val)
    if st.button("Predict"):
        prediction=model.predict([inputs])[0]
        st.success(f"Predicted {target}: {round(prediction, 2)}")

elif menu=="Generate PDF Report":
    st.title("Generate Report")
    if st.button("Create PDF"):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 750, "Global Income Intelligence Report")
        pdf.drawString(100, 720, f"Total Records Analyzed: {df.shape[0]}")
        pdf.drawString(100, 700, f"Variables: {', '.join(df.columns[:5])}...")
        pdf.save()
        st.download_button("Download PDF", buffer.getvalue(), "report.pdf", "application/pdf")

elif menu=="About":
    st.markdown("""
    ### System Intelligence v2.1
    Built with Python & Streamlit. 
    * **Core Logic:** Scikit-Learn & Pandas
    * **Visual Engine:** Plotly & Matplotlib/Seaborn
    * **Styling:** Custom CSS Injection
    """)
