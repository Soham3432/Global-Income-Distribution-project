import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(
    page_title="AI Enterprise Analytics Dashboard",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main-title{
font-size:40px;
font-weight:700;
text-align:center;
margin-bottom:30px;
}

.glass{
background: rgba(255,255,255,0.1);
padding:20px;
border-radius:15px;
backdrop-filter: blur(10px);
}

</style>
""",unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown("<div class='main-title'>AI Enterprise Analytics Dashboard</div>",unsafe_allow_html=True)

# ---------------- FILE UPLOAD ---------------- #

file = st.file_uploader("Upload Dataset (CSV)", type=["csv"])

if file is None:
    st.info("Upload a dataset to start.")
    st.stop()

df = pd.read_csv(file)

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

st.write("Dataset Preview")
st.dataframe(df.head())

# ---------------- MENU ---------------- #

menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "🌍 3D Globe",
        "📈 Advanced Charts",
        "🤖 ML Prediction",
        "🧠 ML Forecast",
        "💡 AI Insights"
    ]
)

# ---------------- DASHBOARD ---------------- #

if menu=="📊 Dashboard":

    st.subheader("Key Metrics")

    col1,col2,col3 = st.columns(3)

    col1.metric("Rows",len(df))
    col2.metric("Columns",len(df.columns))
    col3.metric("Numeric Features",len(numeric_cols))

    if numeric_cols:

        fig = px.histogram(df,x=numeric_cols[0])

        st.plotly_chart(fig,use_container_width=True)

# ---------------- 3D GLOBE ---------------- #

elif menu=="🌍 3D Globe":

    st.subheader("3D Global Visualization")

    lat_col=[c for c in df.columns if "lat" in c.lower()]
    lon_col=[c for c in df.columns if "lon" in c.lower()]

    if lat_col and lon_col:

        fig = px.scatter_geo(
            df,
            lat=lat_col[0],
            lon=lon_col[0],
            size=numeric_cols[0] if numeric_cols else None,
            projection="orthographic"
        )

        fig.update_layout(height=700)

        st.plotly_chart(fig,use_container_width=True)

    else:
        st.warning("Dataset needs latitude and longitude columns.")

# ---------------- ADVANCED CHARTS ---------------- #

elif menu=="📈 Advanced Charts":

    st.subheader("Advanced Visualizations")

    if len(numeric_cols)>=2:

        fig = px.scatter(
            df,
            x=numeric_cols[0],
            y=numeric_cols[1],
            color=numeric_cols[1],
            size=numeric_cols[0],
            template="plotly_dark"
        )

        st.plotly_chart(fig,use_container_width=True)

        fig2 = px.box(df,y=numeric_cols[0])
        st.plotly_chart(fig2,use_container_width=True)

# ---------------- ML PREDICTION ---------------- #

elif menu=="🤖 ML Prediction":

    st.subheader("Prediction by Year")

    year_cols=[c for c in df.columns if "year" in c.lower()]

    if not year_cols:

        st.error("Dataset must contain a Year column.")
        st.stop()

    year_col=year_cols[0]

    target = st.selectbox("Target Variable", numeric_cols)

    X=df[[year_col]]
    y=df[target]

    model=LinearRegression()
    model.fit(X,y)

    year_input = st.slider(
        "Select Year",
        int(df[year_col].min()),
        int(df[year_col].max()+10),
        int(df[year_col].mean())
    )

    if st.button("Predict"):

        prediction=model.predict([[year_input]])[0]

        st.success(f"Predicted {target} for {year_input}: {round(prediction,2)}")

        fig = px.scatter(df,x=year_col,y=target)

        fig.add_scatter(
            x=[year_input],
            y=[prediction],
            mode="markers",
            marker=dict(size=15,color="red"),
            name="Prediction"
        )

        st.plotly_chart(fig,use_container_width=True)

# ---------------- ML FORECAST ---------------- #

elif menu=="🧠 ML Forecast":

    st.subheader("Future Forecast")

    year_cols=[c for c in df.columns if "year" in c.lower()]

    if not year_cols:

        st.error("Dataset must contain a Year column.")
        st.stop()

    year_col=year_cols[0]

    target = st.selectbox("Target Variable", numeric_cols)

    X=df[[year_col]]
    y=df[target]

    model=RandomForestRegressor()
    model.fit(X,y)

    future_year = st.slider(
        "Future Year",
        int(df[year_col].min()),
        int(df[year_col].max()+20),
        int(df[year_col].max()+5)
    )

    if st.button("Forecast"):

        prediction=model.predict([[future_year]])[0]

        st.success(f"Forecasted {target} for {future_year}: {round(prediction,2)}")

        fig = px.line(df,x=year_col,y=target)

        fig.add_scatter(
            x=[future_year],
            y=[prediction],
            mode="markers",
            marker=dict(size=15,color="orange"),
            name="Forecast"
        )

        st.plotly_chart(fig,use_container_width=True)

# ---------------- AI INSIGHTS ---------------- #

elif menu=="💡 AI Insights":

    st.subheader("Automatic Insight Generator")

    insights=[]

    for col in numeric_cols:

        mean=df[col].mean()
        std=df[col].std()
        max_val=df[col].max()
        min_val=df[col].min()

        insight=f"""
        {col}

        Average: {round(mean,2)}
        Highest: {round(max_val,2)}
        Lowest: {round(min_val,2)}
        Std Dev: {round(std,2)}
        """

        insights.append(insight)

    for i in insights:

        st.info(i)
