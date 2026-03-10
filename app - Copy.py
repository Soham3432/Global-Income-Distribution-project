import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import time

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Global Income Intelligence", layout="wide")

# ---------------------------------------------------
# ADVANCED UI STYLE
# ---------------------------------------------------

st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#0f0030,#050010,#000000);
color:white;
font-family:Segoe UI;
}

.logo{
font-size:40px;
font-weight:800;
text-align:center;
background: linear-gradient(90deg,#8b5cf6,#22d3ee);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.card{
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:20px;
box-shadow:0 20px 60px rgba(0,0,0,0.7);
transition:0.3s;
}

.card:hover{
transform:translateY(-6px) scale(1.02);
}

.stButton>button{
background:linear-gradient(90deg,#7c3aed,#22d3ee);
border:none;
border-radius:10px;
padding:8px 25px;
color:white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='logo'>🌍 GLOBAL INCOME INTELLIGENCE</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns

# ---------------------------------------------------
# LOGIN
# ---------------------------------------------------

if "login" not in st.session_state:
    st.session_state.login=False

if not st.session_state.login:

    st.title("Secure Login")

    u=st.text_input("Username")
    p=st.text_input("Password",type="password")

    if st.button("Login"):

        if u=="admin" and p=="1234":
            st.session_state.login=True
            st.rerun()
        else:
            st.error("Invalid Login")

    st.stop()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

menu = st.sidebar.selectbox("Navigation", [

"Executive Dashboard",
"3D Globe Analytics",
"WebGL 3D Dashboard",
"Real-Time Data Stream",
"Dataset Explorer",
"Advanced Charts",
"Machine Learning Prediction",
"Auto ML System",
"AI Data Chatbot",
"Voice Command Analytics",
"Generate PDF Report",
"Dashboard Guide",
"Charts Explainer",
"FAQ",
"About"

])

# ---------------------------------------------------
# EXECUTIVE DASHBOARD
# ---------------------------------------------------

if menu=="Executive Dashboard":

    st.title("Executive Dashboard")

    c1,c2,c3=st.columns(3)

    with c1:
        st.metric("Rows",df.shape[0])

    with c2:
        st.metric("Columns",df.shape[1])

    with c3:
        st.metric("Numeric Variables",len(numeric_cols))

    fig=px.histogram(df,x=numeric_cols[0],template="plotly_dark")

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# 3D ROTATING GLOBE
# ---------------------------------------------------

elif menu=="3D Globe Analytics":

    st.title("3D Rotating Globe Analytics")

    lat = np.random.uniform(-90,90,100)
    lon = np.random.uniform(-180,180,100)

    fig = go.Figure(go.Scattergeo(
        lat=lat,
        lon=lon,
        mode='markers',
        marker=dict(size=6,color="purple")
    ))

    fig.update_layout(
        geo=dict(
            projection_type="orthographic",
            showland=True,
            landcolor="rgb(30,30,30)"
        ),
        template="plotly_dark"
    )

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# WEBGL 3D DASHBOARD
# ---------------------------------------------------

elif menu=="WebGL 3D Dashboard":

    st.title("WebGL 3D Data Visualization")

    x=df[numeric_cols[0]][:200]
    y=df[numeric_cols[1]][:200]
    z=df[numeric_cols[2]][:200]

    fig=go.Figure(data=[go.Scatter3d(
        x=x,y=y,z=z,
        mode="markers",
        marker=dict(size=5,color=z,colorscale="Viridis")
    )])

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# REAL TIME DATA
# ---------------------------------------------------

elif menu=="Real-Time Data Stream":

    st.title("Real-Time Data Pipeline Simulation")

    chart=st.line_chart(np.random.randn(10,3))

    for i in range(30):
        new=np.random.randn(1,3)
        chart.add_rows(new)
        time.sleep(0.2)

# ---------------------------------------------------
# DATASET EXPLORER
# ---------------------------------------------------

elif menu=="Dataset Explorer":

    st.title("Dataset Explorer")

    st.dataframe(df)

    col=st.selectbox("Column",df.columns)

    st.write(df[col].describe())

# ---------------------------------------------------
# ADVANCED CHARTS
# ---------------------------------------------------

elif menu=="Advanced Charts":

    chart=st.selectbox("Chart Type",[
    "3D Scatter","Bubble","Heatmap","Radar"
    ])

    if chart=="3D Scatter":

        x=st.selectbox("X",numeric_cols)
        y=st.selectbox("Y",numeric_cols)
        z=st.selectbox("Z",numeric_cols)

        fig=px.scatter_3d(df,x=x,y=y,z=z,color=z)

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Bubble":

        x=st.selectbox("X axis",numeric_cols)
        y=st.selectbox("Y axis",numeric_cols)

        fig=px.scatter(df,x=x,y=y,size=numeric_cols[0],color=numeric_cols[0])

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Heatmap":

        corr=df[numeric_cols].corr()

        fig=px.imshow(corr,text_auto=True)

        st.plotly_chart(fig,use_container_width=True)

    elif chart=="Radar":

        sample=df[numeric_cols].mean()

        fig=go.Figure()

        fig.add_trace(go.Scatterpolar(
        r=sample.values,
        theta=sample.index,
        fill="toself"
        ))

        st.plotly_chart(fig,use_container_width=True)

# ---------------------------------------------------
# MACHINE LEARNING
# ---------------------------------------------------

elif menu=="Machine Learning Prediction":

    st.title("ML Prediction")

    target=st.selectbox("Target",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    model=LinearRegression()
    model.fit(X,y)

    inputs=[]

    for col in features:
        val=st.number_input(col,value=float(X[col].mean()))
        inputs.append(val)

    if st.button("Predict"):

        pred=model.predict([inputs])[0]

        st.success(pred)

# ---------------------------------------------------
# AUTO ML
# ---------------------------------------------------

elif menu=="Auto ML System":

    st.title("Auto Machine Learning")

    target=st.selectbox("Target Variable",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features].fillna(0)
    y=df[target].fillna(0)

    models={
    "Linear Regression":LinearRegression(),
    "Random Forest":RandomForestRegressor(),
    "Gradient Boosting":GradientBoostingRegressor()
    }

    scores={}

    for name,m in models.items():

        m.fit(X,y)
        pred=m.predict(X)
        score=r2_score(y,pred)

        scores[name]=score

    best=max(scores,key=scores.get)

    st.write("Model Scores:",scores)

    st.success(f"Best Model: {best}")

# ---------------------------------------------------
# AI CHATBOT
# ---------------------------------------------------

elif menu=="AI Data Chatbot":

    st.title("AI Data Assistant")

    question=st.text_input("Ask about dataset")

    if question:

        if "rows" in question.lower():
            st.write(f"Dataset has {df.shape[0]} rows")

        elif "columns" in question.lower():
            st.write(f"Dataset has {df.shape[1]} columns")

        elif "average" in question.lower():
            st.write(df[numeric_cols].mean())

        else:
            st.write("Try asking about rows, columns, averages")

# ---------------------------------------------------
# VOICE COMMAND
# ---------------------------------------------------

elif menu=="Voice Command Analytics":

    st.title("Voice Command")

    st.markdown("""
Press the button and speak commands like:

• show rows  
• show columns  
• show average  
""")

    st.components.v1.html("""
    <button onclick="start()">Start Voice Command</button>
    <p id="output"></p>

<script>

function start(){
var rec = new webkitSpeechRecognition();
rec.onresult=function(e){
document.getElementById("output").innerHTML=e.results[0][0].transcript;
}
rec.start();
}

</script>
""",height=200)

# ---------------------------------------------------
# PDF REPORT
# ---------------------------------------------------

elif menu=="Generate PDF Report":

    if st.button("Create PDF"):

        buffer=io.BytesIO()

        pdf=canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button("Download PDF",buffer.getvalue(),"report.pdf")

# ---------------------------------------------------
# DASHBOARD GUIDE
# ---------------------------------------------------

elif menu=="Dashboard Guide":

    st.title("Dashboard Guide")

    st.markdown("""

### How to Use the Dashboard

1. **Executive Dashboard**
Overview of dataset statistics.

2. **3D Globe Analytics**
View global distribution visually.

3. **Advanced Charts**
Explore relationships between variables.

4. **Machine Learning**
Predict values using trained models.

5. **Auto ML**
Automatically finds best ML model.

6. **AI Chatbot**
Ask questions about the dataset.

7. **Real-Time Data**
Simulated live analytics.

""")

# ---------------------------------------------------
# CHART EXPLAINER
# ---------------------------------------------------

elif menu=="Charts Explainer":

    st.title("Charts Explained")

    st.markdown("""

### Scatter Plot
Shows relationship between two variables.

### Bubble Chart
Adds third dimension using bubble size.

### Heatmap
Shows correlation between variables.

### Radar Chart
Compares multiple metrics simultaneously.

### 3D Scatter
Displays relationships across three variables.

""")

# ---------------------------------------------------
# FAQ
# ---------------------------------------------------

elif menu=="FAQ":

    st.title("FAQ")

    st.markdown("""

**Q: What dataset is used?**  
Income distribution dataset.

**Q: What ML models are used?**  
Linear Regression, Random Forest, Gradient Boosting.

**Q: Can I upload my own dataset?**  
You can modify the code to load another CSV.

**Q: Does this support real-time data?**  
Currently simulated but can connect to APIs.

""")

# ---------------------------------------------------
# ABOUT
# ---------------------------------------------------

elif menu=="About":

    st.markdown("""

### Global Income Intelligence Platform

Features:

• 3D visualizations  
• AI chatbot  
• Auto ML system  
• Voice command analytics  
• Real-time streaming  
• WebGL dashboards  

Built using **Streamlit + Plotly + Machine Learning**

""")
