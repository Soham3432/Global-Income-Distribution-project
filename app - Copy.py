import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------
# DYNAMIC UI THEME ENGINE
# ---------------------------------------------------
st.sidebar.title("🎨 UI Settings")
theme_color = st.sidebar.color_picker("Accent Color", "#7c3aed")
glow_effect = st.sidebar.slider("Glow Intensity", 0, 20, 10)

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, #050010 0%, #0d0026 50%, #1a0040 100%);
        color: white;
    }}
    .title {{
        font-size: 50px;
        font-weight: 900;
        text-align: center;
        color: {theme_color};
        text-shadow: 0 0 {glow_effect}px {theme_color};
        margin-bottom: 30px;
    }}
    /* Custom Card Style */
    .metric-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid {theme_color}44;
        border-radius: 15px;
        padding: 20px;
        transition: 0.3s;
    }}
    .metric-card:hover {{
        border: 1px solid {theme_color};
        box-shadow: 0 0 {glow_effect}px {theme_color}66;
    }}
    .stButton>button {{
        background: {theme_color} !important;
        box-shadow: 0 0 {glow_effect}px {theme_color}aa;
        border: none; color: white; border-radius: 8px;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA INITIALIZATION
# ---------------------------------------------------
@st.cache_data
def load_data():
    try:
        return pd.read_csv("final.sheet.csv")
    except:
        # Generate high-dimensional dummy data if file is missing
        data = np.random.randn(200, 5)
        return pd.DataFrame(data, columns=['Income_Index', 'GDP_Growth', 'Education_Rank', 'Tech_Adoption', 'Stability'])

df = load_data()
numeric_cols = df.select_dtypes(include=[np.number]).columns

# ---------------------------------------------------
# NAVIGATION
# ---------------------------------------------------
menu = st.sidebar.selectbox("Navigation", [
    "Advanced Plotly Explorer",
    "Executive Dashboard", 
    "ML Predictor",
    "Dataset Explorer"
])

# ---------------------------------------------------
# ADVANCED PLOTLY EXPLORER (EXPANDED)
# ---------------------------------------------------
if menu == "Advanced Plotly Explorer":
    st.markdown("<div class='title'>3D Multi-Dimensional Analysis</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["3D Hyper-Visuals", "Relational Mapping", "Polar Intelligence"])

    with tab1:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.subheader("Controls")
            x_ax = st.selectbox("X Axis", numeric_cols, key="x1")
            y_ax = st.selectbox("Y Axis", numeric_cols, key="y1")
            z_ax = st.selectbox("Z Axis", numeric_cols, key="z1")
            c_scale = st.selectbox("Color Palette", ["Viridis", "Magma", "Electric", "Hot"])
        
        with col2:
            # 3D Mesh / Surface logic
            fig = go.Figure(data=[go.Mesh3d(
                x=df[x_ax], y=df[y_ax], z=df[z_ax],
                intensity=df[z_ax],
                colorscale=c_scale,
                opacity=0.50,
                showscale=True
            )])
            
            # Adding Scatter points on top of Mesh for detail
            fig.add_trace(go.Scatter3d(
                x=df[x_ax], y=df[y_ax], z=df[z_ax],
                mode='markers',
                marker=dict(size=4, color='white', opacity=0.8)
            ))

            fig.update_layout(
                template="plotly_dark",
                margin=dict(l=0, r=0, b=0, t=0),
                scene=dict(
                    xaxis_title=x_ax, yaxis_title=y_ax, zaxis_title=z_ax,
                    xaxis=dict(gridcolor=theme_color+"33"),
                    yaxis=dict(gridcolor=theme_color+"33"),
                    zaxis=dict(gridcolor=theme_color+"33"),
                )
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("Interactive Correlation Matrix")
        corr = df[numeric_cols].corr()
        fig_corr = px.imshow(
            corr, 
            text_auto=True, 
            aspect="auto",
            color_continuous_scale=[[0, "#000000"], [1, theme_color]],
            template="plotly_dark"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    with tab3:
        st.subheader("Radial Performance Metrics")
        # Radar chart for the first 5 rows
        categories = numeric_cols.tolist()
        fig_radar = go.Figure()

        for i in range(min(3, len(df))):
            fig_radar.add_trace(go.Scatterpolar(
                r=df.iloc[i][numeric_cols].values,
                theta=categories,
                fill='toself',
                name=f'Record {i}'
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, df[numeric_cols].max().max()])),
            template="plotly_dark",
            showlegend=True
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ---------------------------------------------------
# EXECUTIVE DASHBOARD (RESTYLED)
# ---------------------------------------------------
elif menu == "Executive Dashboard":
    st.markdown("<div class='title'>Platform Intelligence</div>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"<div class='metric-card'><h3>Records</h3><h2>{df.shape[0]}</h2></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><h3>Features</h3><h2>{df.shape[1]}</h2></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><h3>Nulls</h3><h2>{df.isna().sum().sum()}</h2></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='metric-card'><h3>D-Type</h3><h2>Float64</h2></div>", unsafe_allow_html=True)

    st.markdown("---")
    # Animated Growth Chart
    st.subheader("Temporal Trend Simulation")
    fig_anim = px.area(df, y=numeric_cols[0], template="plotly_dark", color_discrete_sequence=[theme_color])
    fig_anim.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig_anim, use_container_width=True)

# ---------------------------------------------------
# ML PREDICTOR
# ---------------------------------------------------
elif menu == "ML Predictor":
    st.markdown("<div class='title'>Predictive Engine</div>", unsafe_allow_html=True)
    
    target = st.selectbox("Select Target Variable", numeric_cols)
    feats = [c for c in numeric_cols if c != target]
    
    X = df[feats].fillna(df[feats].mean())
    y = df[target].fillna(df[target].mean())
    
    model = LinearRegression().fit(X, y)
    
    st.write("Adjust input parameters to simulate outcomes:")
    inputs = []
    input_cols = st.columns(len(feats))
    for i, col in enumerate(feats):
        with input_cols[i]:
            val = st.number_input(col, value=float(X[col].mean()))
            inputs.append(val)
            
    if st.button("Run Simulation"):
        res = model.predict([inputs])[0]
        st.balloons()
        st.markdown(f"""
        <div style="text-align:center; padding:30px; border-radius:20px; background:{theme_color}22; border:2px solid {theme_color}">
            <h1 style="color:{theme_color}">Result: {round(res, 4)}</h1>
        </div>
        """, unsafe_allow_html=True)
