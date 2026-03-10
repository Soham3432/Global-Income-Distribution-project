import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Global Income Intelligence", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("final.sheet.csv")

df = load_data()

numeric_cols = df.select_dtypes(include=["int64","float64"]).columns
categorical_cols = df.select_dtypes(include=["object"]).columns


# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

st.sidebar.title("🌍 Global Income Platform")

menu = st.sidebar.radio(
"Navigation",
[
"Executive Dashboard",
"Power BI Dashboard",
"Dataset Explorer",
"Chart Explorer",
"Country Analysis",
"Machine Learning Prediction",
"Generate PDF Report",
"FAQ",
"About"
]
)

# -----------------------------
# EXECUTIVE DASHBOARD
# -----------------------------

if menu=="Executive Dashboard":

    st.title("Executive Dashboard")

    col1,col2,col3 = st.columns(3)

    col1.metric("Rows",df.shape[0])
    col2.metric("Columns",df.shape[1])
    col3.metric("Numeric Variables",len(numeric_cols))

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    fig,ax = plt.subplots()

    df[numeric_cols[0]].hist(ax=ax)

    st.pyplot(fig)

# -----------------------------
# DATASET EXPLORER
# -----------------------------

elif menu=="Dataset Explorer":

    st.title("Dataset Explorer")

    st.dataframe(df)

    column = st.selectbox("Select Column",df.columns)

    st.write(df[column].describe())

    st.subheader("Missing Values")

    st.write(df.isnull().sum())


# -----------------------------
# CHART EXPLORER
# -----------------------------

elif menu=="Chart Explorer":

    st.title("Chart Explorer")

    chart_type = st.selectbox(
    "Choose Chart",
    ["Histogram","Boxplot","Scatter","Bar","Line","Pie"]
    )

    column = st.selectbox("Select Column",df.columns)

    fig,ax = plt.subplots()

    if chart_type=="Histogram":

        sns.histplot(df[column],ax=ax)

        explanation="""
        Histogram shows the distribution of values.
        Helps identify skewness and spread of the dataset.
        """

    elif chart_type=="Boxplot":

        sns.boxplot(x=df[column],ax=ax)

        explanation="""
        Boxplot shows median, quartiles, and outliers.
        Useful for detecting extreme values.
        """

    elif chart_type=="Scatter":

        col2 = st.selectbox("Second Column",numeric_cols)

        sns.scatterplot(x=df[column],y=df[col2],ax=ax)

        explanation="""
        Scatter plot shows relationship between two variables.
        """

    elif chart_type=="Bar":

        df[column].value_counts().plot(kind="bar",ax=ax)

        explanation="Bar chart compares categorical values."

    elif chart_type=="Line":

        df[column].plot(kind="line",ax=ax)

        explanation="Line chart shows trends across index/time."

    elif chart_type=="Pie":

        df[column].value_counts().plot(kind="pie",autopct='%1.1f%%')

        explanation="Pie chart shows proportional distribution."

    st.pyplot(fig)

    st.info(explanation)

# -----------------------------
# ML PREDICTION
# -----------------------------

elif menu=="Machine Learning Prediction":

    st.title("Machine Learning Prediction")

    target = st.selectbox("Target Variable",numeric_cols)

    features=[c for c in numeric_cols if c!=target]

    X=df[features]
    y=df[target]

    model=LinearRegression()

    model.fit(X,y)

    inputs=[]

    for col in features:

        val=st.number_input(col,value=float(X[col].mean()))

        inputs.append(val)

    if st.button("Predict"):

        prediction=model.predict([inputs])[0]

        st.success(f"Predicted {target}: {prediction}")

# -----------------------------
# PDF REPORT
# -----------------------------

elif menu=="Generate PDF Report":

    st.title("Generate PDF Report")

    if st.button("Create Report"):

        buffer = io.BytesIO()

        pdf = canvas.Canvas(buffer)

        pdf.drawString(100,750,"Global Income Report")
        pdf.drawString(100,720,f"Rows: {df.shape[0]}")
        pdf.drawString(100,700,f"Columns: {df.shape[1]}")

        pdf.save()

        st.download_button(
        "Download Report",
        buffer.getvalue(),
        "report.pdf"
        )

# -----------------------------
# FAQ
# -----------------------------

elif menu=="FAQ":

    st.title("Frequently Asked Questions")

    st.markdown("""
**Q1: What does this platform do?**  
Provides data analytics and machine learning insights on income data.

**Q2: What algorithm is used?**  
Linear Regression.

**Q3: Can predictions be trusted?**  
Predictions depend on dataset quality.

**Q4: What visualizations are supported?**  
Matplotlib and Seaborn charts.

**Q5: Can data be exported?**  
Yes, via dataset explorer.
""")

# -----------------------------
# ABOUT
# -----------------------------

elif menu=="About":

    st.title("About Platform")

    st.write("""
Global Income Intelligence Platform built with:

• Streamlit  
• Python  
• Machine Learning  
• Data Visualization  
• Power BI Integration
""")
