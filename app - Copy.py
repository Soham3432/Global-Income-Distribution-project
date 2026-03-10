import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas
import io
import time

st.set_page_config(page_title="Global Income Intelligence Platform", layout="wide")

# --------------------------------------------------
# 3D DARK UI STYLE
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#020617,#020617,#0f172a,#020617);
color:white;
font-family:'Segoe UI';
}

.main-title{
font-size:52px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#3b82f6,#22c55e,#ec4899);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.card{
background:rgba(255,255,255,0.04);
padding:20px;
border-radius:14px;
text-align:center;
box-shadow:0 10px 40px rgba(59,130,246,0.35);
}

.topnav{
text-align:center;
padding:10px;
margin-bottom:20px;
}

button[kind="secondary"]{
background:#111827;
color:white;
border-radius:8px;
padding:6px 14px;
margin:3px;
border:1px solid #374151;
}

button[kind="secondary"]:hover{
background:#1f2937;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.markdown("<div class='main-title'>Global Income Intelligence Platform</div>",unsafe_allow_html=True)

    user=st.text_input("Username")
    pw=st.text_input("Password",type="password")

    if st.button("Login"):
        if user=="admin" and pw=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# --------------------------------------------------
# NAVIGATION CENTER FILTER BUTTONS
# --------------------------------------------------

st.markdown("<div class='topnav'>",unsafe_allow_html=True)
menu = st.radio("",
[
"Dashboard",
"Upload Dataset",
"Chart Explorer",
"Chart Explainer",
"Statistics Lab",
"AI Insights",
"Correlation Analyzer",
"Auto Dashboard",
"Forecasting",
"Machine Learning",
"Report",
"FAQ"
],horizontal=True)
st.markdown("</div>",unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

if "data" not in st.session_state:
    st.session_state.data = load_data()

df = st.session_state.data

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# --------------------------------------------------
# DASHBOARD WITH ANIMATED KPI
# --------------------------------------------------

if menu=="Dashboard":

    st.markdown("<div class='main-title'>Executive Dashboard</div>",unsafe_allow_html=True)

    def animated_counter(label,value):
        placeholder=st.empty()
        for i in range(int(value)):
            placeholder.markdown(f"""<div class='card'><h2>{i}</h2>{label}</div>""",unsafe_allow_html=True)
            time.sleep(0.01)
        placeholder.markdown(f"""<div class='card'><h2>{value}</h2>{label}</div>""",unsafe_allow_html=True)

    c1,c2,c3,c4=st.columns(4)

    with c1:
        animated_counter("Records",df.shape[0])

    with c2:
        animated_counter("Columns",df.shape[1])

    with c3:
        animated_counter("Numeric",len(numeric_cols))

    with c4:
        animated_counter("Categorical",len(categorical_cols))

    if len(numeric_cols)>0:

        fig,ax = plt.subplots(figsize=(4,3))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.hist(df[numeric_cols[0]], bins=30, color="#3b82f6")
        ax.set_title("Distribution")

        st.pyplot(fig)

# --------------------------------------------------
# DATASET UPLOAD
# --------------------------------------------------

elif menu=="Upload Dataset":

    st.title("Upload Your Dataset")

    file=st.file_uploader("Upload CSV",type=["csv"])

    if file:

        st.session_state.data=pd.read_csv(file)

        st.success("Dataset Loaded")

        st.dataframe(st.session_state.data.head(100))

# --------------------------------------------------
# CHART EXPLORER (SMALL CHARTS)
# --------------------------------------------------

elif menu=="Chart Explorer":

    st.title("Chart Explorer")

    chart=st.selectbox("Chart Type",
    ["Bar","Pie","Line","Scatter"])

    if chart=="Bar":

        col=st.selectbox("Column",numeric_cols)

        fig,ax=plt.subplots(figsize=(4,3))
        fig.patch.set_facecolor("white")
        ax.bar(range(len(df[col])),df[col],color="#22c55e")

        st.pyplot(fig)

    elif chart=="Pie":

        col=st.selectbox("Category",categorical_cols)

        data=df[col].value_counts()

        fig,ax=plt.subplots(figsize=(4,3))
        fig.patch.set_facecolor("white")

        ax.pie(data.values,labels=data.index,
               colors=["#3b82f6","#22c55e","#ec4899","#facc15"])

        st.pyplot(fig)

    elif chart=="Line":

        col=st.selectbox("Column",numeric_cols)

        fig,ax=plt.subplots(figsize=(4,3))
        fig.patch.set_facecolor("white")

        ax.plot(df[col],color="#ec4899")

        st.pyplot(fig)

    elif chart=="Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)

        fig,ax=plt.subplots(figsize=(4,3))
        fig.patch.set_facecolor("white")

        ax.scatter(df[x],df[y],color="#3b82f6")

        st.pyplot(fig)

# --------------------------------------------------
# CHART EXPLAINER
# --------------------------------------------------

elif menu=="Chart Explainer":

    st.title("Chart Explainer for Business Dashboards")

    explanations={

    "Bar Chart":"""
Bar charts compare categories. They are widely used in Power BI dashboards
for sales comparison, country level income comparison, KPI ranking and
performance analysis.

Business Use Cases:
- Comparing revenue across regions
- Department performance tracking
- Category level distribution
""",

    "Line Chart":"""
Line charts are used to analyze trends over time.

Business Use Cases:
- Sales growth trends
- Time series forecasting
- Monthly revenue tracking
""",

    "Pie Chart":"""
Pie charts display percentage distribution.

Business Use Cases:
- Market share
- Product contribution
- Expense breakdown
""",

    "Scatter Plot":"""
Scatter plots identify relationships between variables.

Business Use Cases:
- Correlation analysis
- Risk vs return analysis
- Customer segmentation
"""
    }

    chart=st.selectbox("Select Chart",list(explanations.keys()))

    st.write(explanations[chart])

# --------------------------------------------------
# STATISTICS LAB
# --------------------------------------------------

elif menu=="Statistics Lab":

    st.title("Statistical Analysis")

    col=st.selectbox("Column",numeric_cols)

    st.write(df[col].describe())

    fig,ax=plt.subplots(figsize=(4,3))
    fig.patch.set_facecolor("white")

    ax.boxplot(df[col])

    st.pyplot(fig)

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

elif menu=="AI Insights":

    st.title("Automated Data Insights")

    st.write("Dataset Shape:",df.shape)

    st.write("Missing Values:")

    st.write(df.isnull().sum())

    st.write("Top Correlations")

    st.write(df.corr(numeric_only=True))

# --------------------------------------------------
# CORRELATION ANALYZER
# --------------------------------------------------

elif menu=="Correlation Analyzer":

    st.title("Correlation Heatmap")

    corr=df.corr(numeric_only=True)

    fig,ax=plt.subplots(figsize=(5,4))

    cax=ax.imshow(corr,cmap="coolwarm")

    fig.colorbar(cax)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns,rotation=90)

    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)

    st.pyplot(fig)

# --------------------------------------------------
# AUTO DASHBOARD
# --------------------------------------------------

elif menu=="Auto Dashboard":

    st.title("Automatic Chart Generator")

    for col in numeric_cols:

        fig,ax=plt.subplots(figsize=(4,3))
        fig.patch.set_facecolor("white")

        ax.hist(df[col],color="#3b82f6")

        ax.set_title(col)

        st.pyplot(fig)

# --------------------------------------------------
# FORECASTING
# --------------------------------------------------

elif menu=="Forecasting":

    st.title("Time Series Forecasting")

    col=st.selectbox("Target",numeric_cols)

    df["time_index"]=range(len(df))

    X=df[["time_index"]]
    y=df[col]

    model=LinearRegression()

    model.fit(X,y)

    future=st.slider("Future Steps",1,50,10)

    future_index=np.arange(len(df),len(df)+future).reshape(-1,1)

    pred=model.predict(future_index)

    fig,ax=plt.subplots(figsize=(5,3))
    fig.patch.set_facecolor("white")

    ax.plot(df[col],color="#3b82f6")
    ax.plot(range(len(df),len(df)+future),pred,color="#ec4899")

    st.pyplot(fig)

# --------------------------------------------------
# MACHINE LEARNING
# --------------------------------------------------

elif menu=="Machine Learning":

    st.title("Prediction Model")

    target=st.selectbox("Target",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    model=RandomForestRegressor()

    model.fit(X,y)

    inputs=[]

    for col in features:

        val=st.number_input(col,value=float(X[col].mean()))

        inputs.append(val)

    if st.button("Predict"):

        pred=model.predict([inputs])[0]

        st.success(f"Predicted Value: {pred}")

        st.write("Model R2 Score:",r2_score(y,model.predict(X)))

# --------------------------------------------------
# REPORT
# --------------------------------------------------

elif menu=="Report":

    if st.button("Generate PDF Report"):

        buffer=io.BytesIO()

        pdf=canvas.Canvas(buffer)

        pdf.drawString(100,750,"Income Analytics Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button("Download",buffer.getvalue(),"report.pdf")

# --------------------------------------------------
# FAQ (COMPLEX Q/A)
# --------------------------------------------------

elif menu=="FAQ":

    st.title("Advanced FAQ for Analytics Platform")

    faq={

"What insights can analysts derive from this dashboard?":
"""
The platform enables analysts to explore data distributions, correlations,
trend patterns and predictive insights. By combining statistical analysis,
visual exploration and machine learning models, analysts can identify
hidden relationships within the dataset.
""",

"How does forecasting help business decisions?":
"""
Forecasting models estimate future trends based on historical data.
Businesses use these predictions to plan budgets, manage resources,
and anticipate market demand.
""",

"Why is correlation analysis important?":
"""
Correlation analysis helps determine whether two variables move together.
Understanding these relationships helps analysts identify drivers of
business performance.
""",

"What role does machine learning play in analytics dashboards?":
"""
Machine learning enables predictive analytics. Instead of only visualizing
past data, the dashboard can estimate future outcomes and identify patterns
that traditional statistical analysis may miss.
"""

}

    q=st.selectbox("Question",list(faq.keys()))

    st.write(faq[q])
