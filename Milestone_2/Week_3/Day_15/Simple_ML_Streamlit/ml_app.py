# modern_app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib, json, plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =============== PAGE CONFIG ===============
st.set_page_config(
    page_title="Dinesh's Botanical Iris Lab 🌸",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============== MODERN BOTANICAL THEME ===============
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Modern botanical gradient theme */
    .stApp {
        background: 
            linear-gradient(135deg, 
                #667eea 0%, 
                #764ba2 25%, 
                #f093fb 50%, 
                #f5576c 75%, 
                #4facfe 100%);
        background-size: 400% 400%;
        animation: gradient-shift 15s ease infinite;
        font-family: 'Poppins', sans-serif;
        color: #2d3748;
        min-height: 100vh;
        position: relative;
    }

    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Floating botanical elements */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        animation: float-pattern 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }

    @keyframes float-pattern {
        0% { transform: translate(0, 0); }
        25% { transform: translate(-10px, -15px); }
        50% { transform: translate(10px, -10px); }
        75% { transform: translate(-5px, 15px); }
        100% { transform: translate(0, 0); }
    }

    /* Glass morphism sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    section[data-testid="stSidebar"] .css-1d391kg {
        color: #2d3748 !important;
    }

    /* Elegant gradient headings */
    h1 {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 50%, #2d3748 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        text-align: center;
        font-size: 3.5rem !important;
        font-family: 'Poppins', sans-serif;
        margin-bottom: 2rem !important;
        position: relative;
    }

    h1::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
    }

    h2, h3 {
        color: #2d3748;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
    }

    /* Modern glass cards */
    .prediction-card {
        background: rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.5);
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
    }

    .data-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .data-card:hover {
        transform: translateY(-3px);
    }

    /* Elegant buttons with hover effects */
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 2.5rem;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        text-transform: none;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
    }

    div.stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.3), 
            transparent);
        transition: left 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    div.stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 15px 40px rgba(102, 126, 234, 0.4),
            inset 0 2px 0 rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }

    div.stButton > button:hover::before {
        left: 100%;
    }

    div.stButton > button:active {
        transform: translateY(-1px) scale(0.98);
    }

    /* Beautiful sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 12px;
        height: 8px !important;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(135deg, #ffffff, #f7fafc) !important;
        box-shadow: 
            0 4px 12px rgba(102, 126, 234, 0.3),
            0 2px 4px rgba(0, 0, 0, 0.1);
        border: 3px solid rgba(255, 255, 255, 0.8);
        width: 24px !important;
        height: 24px !important;
        border-radius: 50% !important;
        transition: all 0.3s ease;
    }

    .stSlider > div > div > div > div:hover {
        transform: scale(1.2);
        box-shadow: 
            0 6px 20px rgba(102, 126, 234, 0.4),
            0 3px 6px rgba(0, 0, 0, 0.15);
    }

    /* Enhanced success messages */
    .element-container div[data-testid="alert"] {
        background: rgba(72, 187, 120, 0.15);
        border: 2px solid rgba(72, 187, 120, 0.3);
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }

    /* Radio buttons styling */
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] > p {
        font-weight: 500;
        color: #2d3748;
        font-family: 'Inter', sans-serif;
    }

    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover {
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
    }

    /* Modern metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.35);
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 16px 16px 0 0;
    }

    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.15);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Poppins', sans-serif;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #4a5568;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 0.8rem;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    /* Sidebar title enhancement */
    .sidebar-title {
        background: linear-gradient(135deg, #2d3748, #4a5568);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Poppins', sans-serif;
    }

    /* Floating animation */
    .floating-icon {
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    /* Checkbox styling */
    .stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {
        color: #2d3748 !important;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }

    /* Enhanced dataframe styling */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }

    /* Improved text styling */
    p, li {
        color: #2d3748;
        line-height: 1.7;
        font-family: 'Inter', sans-serif;
    }

    /* Feature label styling */
    .feature-label {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# =============== LOAD RESOURCES ===============
@st.cache_resource
def load_model():
    return joblib.load("models/iris_pipeline.joblib")

@st.cache_data
def load_meta():
    with open("models/feature_stats.json") as f:
        return json.load(f)

@st.cache_data
def load_df():
    return pd.read_csv("data/iris.csv")

model = load_model()
meta = load_meta()
df = load_df()

feature_stats = meta["feature_stats"]
feature_names = meta["feature_names"]
target_names = meta["target_names"]

# =============== SIDEBAR NAVIGATION ===============
st.sidebar.markdown('<h2 class="sidebar-title">🌸 Botanical Control Panel</h2>', unsafe_allow_html=True)

# Add current time with botanical styling
current_time = datetime.now().strftime("%H:%M:%S")
st.sidebar.markdown(f"""
<div class="metric-container">
    <div class="metric-value">{current_time}</div>
    <div class="metric-label">Current Time</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

mode = st.sidebar.radio(
    "🚀 Choose Your Analysis Mode", 
    ["🔮 AI Prediction Engine", "📊 Data Explorer Dashboard"],
    help="Select your preferred analysis mode"
)

# Add enhanced system stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Dataset Overview")

col1, col2 = st.sidebar.columns(2)
with col1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{len(df)}</div>
        <div class="metric-label">Total Samples</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-value">{len(feature_names)}</div>
        <div class="metric-label">Features</div>
    </div>
    """, unsafe_allow_html=True)

# Species distribution
st.sidebar.markdown("### 🌺 Species Distribution")
species_counts = df['target'].value_counts()
for i, (species_idx, count) in enumerate(species_counts.items()):
    species_name = target_names[species_idx]
    st.sidebar.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.2);
        padding: 0.8rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        border-left: 4px solid {'#667eea' if i == 0 else '#764ba2' if i == 1 else '#f093fb'};
        backdrop-filter: blur(5px);
    ">
        <div style="font-weight: 600; color: #2d3748;">{species_name}</div>
        <div style="color: #4a5568; font-size: 0.9rem;">{count} samples</div>
    </div>
    """, unsafe_allow_html=True)

# =============== APP HEADER ===============
st.markdown("""
<h1>🌸 DINESH'S BOTANICAL IRIS LAB</h1>
<div style="text-align: center; margin-bottom: 3rem;">
    <p style="font-size: 1.3rem; color: #4a5568; font-weight: 400; margin-bottom: 0.5rem;">
        Advanced Machine Learning for Iris Species Classification
    </p>
    <p style="color: #718096; font-family: 'Inter', sans-serif; font-size: 1rem;">
        🧠 Powered by Neural Networks • 📈 Real-time Analysis • 🎯 High Precision
    </p>
</div>
""", unsafe_allow_html=True)

# =============== PREDICTION MODE ===============
if mode.startswith("🔮"):
    st.markdown("""
    <div class="prediction-card">
        <h2 style="color: #2d3748; margin-bottom: 1rem;">🤖 AI Prediction Engine</h2>
        <p style="color: #4a5568; font-size: 1.1rem;">Configure the botanical parameters to classify iris species with precision</p>
    """, unsafe_allow_html=True)

    # Feature input grid with enhanced styling
    cols = st.columns(2)
    values = []
    
    for i, fname in enumerate(feature_names):
        stats = feature_stats[fname]
        min_val, max_val, mean_val = stats["min"], stats["max"], stats["mean"]
        
        with cols[i % 2]:
            st.markdown(f'<div class="feature-label">🌿 {fname.replace("_", " ").title()}</div>', unsafe_allow_html=True)
            slider = st.slider(
                label="",
                min_value=float(min_val),
                max_value=float(max_val),
                value=float(mean_val),
                help=f"Range: {min_val:.1f} - {max_val:.1f} | Mean: {mean_val:.1f}",
                key=f"slider_{i}"
            )
            values.append(slider)
            st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Enhanced prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_clicked = st.button("🚀 ANALYZE SPECIMEN", use_container_width=True)

    if predict_clicked:
        with st.spinner("🔬 Analyzing botanical features..."):
            X_input = np.array(values).reshape(1, -1)
            pred = model.predict(X_input)[0]
            probs = model.predict_proba(X_input)[0]
            pred_name = target_names[pred]
            confidence = float(probs[pred])

        # Enhanced results display
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, 
                rgba(72, 187, 120, 0.15) 0%,
                rgba(255, 255, 255, 0.25) 50%,
                rgba(102, 126, 234, 0.15) 100%);
            border: 3px solid rgba(72, 187, 120, 0.4);
            border-radius: 24px;
            padding: 3rem;
            text-align: center;
            margin: 2rem 0;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 40px rgba(72, 187, 120, 0.2);
            position: relative;
            overflow: hidden;
        ">
            <div class="floating-icon" style="font-size: 4rem; margin-bottom: 1rem;">🎯</div>
            <h2 style="color: #22543d; margin-bottom: 1.5rem; font-size: 1.8rem;">Classification Complete!</h2>
            <h1 style="
                background: linear-gradient(135deg, #22543d, #38a169);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 3.5rem; 
                margin: 1rem 0;
                font-family: 'Poppins', sans-serif;
                font-weight: 800;
            ">{pred_name}</h1>
            <div style="
                background: rgba(255, 255, 255, 0.3);
                border-radius: 16px;
                padding: 1rem 2rem;
                margin-top: 1.5rem;
                display: inline-block;
                backdrop-filter: blur(10px);
            ">
                <p style="color: #2d3748; font-size: 1.3rem; margin: 0;">
                    Confidence Level: <span style="color: #22543d; font-weight: 700;">{confidence:.1%}</span>
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Beautiful probability visualization
        prob_df = pd.DataFrame({"Species": target_names, "Probability": list(probs)})
        
        fig = go.Figure()
        
        colors = ['#667eea', '#764ba2', '#f093fb']
        for i, (species, prob) in enumerate(zip(target_names, probs)):
            fig.add_trace(go.Bar(
                x=[species],
                y=[prob],
                name=species,
                marker_color=colors[i],
                marker_line=dict(color='white', width=3),
                text=f'{prob:.2%}',
                textposition='outside',
                textfont=dict(color='#2d3748', size=16, family='Poppins', weight='bold'),
                hovertemplate=f'<b>{species}</b><br>Probability: {prob:.2%}<br><extra></extra>',
                opacity=0.9
            ))

        fig.update_layout(
            title={
                'text': '🧠 Model Confidence Analysis',
                'x': 0.5,
                'font': {'size': 24, 'color': '#2d3748', 'family': 'Poppins', 'weight': 'bold'}
            },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255, 255, 255, 0.1)',
            font=dict(color='#2d3748', family='Inter'),
            showlegend=False,
            height=450,
            yaxis=dict(
                range=[0, 1.1],
                title='Probability Score',
                gridcolor='rgba(255, 255, 255, 0.3)',
                tickformat='.0%',
                title_font=dict(size=14, family='Inter')
            ),
            xaxis=dict(
                title='Iris Species',
                gridcolor='rgba(255, 255, 255, 0.3)',
                title_font=dict(size=14, family='Inter')
            ),
            margin=dict(t=80, b=60, l=60, r=60)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =============== DATA EXPLORATION MODE ===============
else:
    st.markdown("""
    <div class="data-card">
        <h2 style="color: #2d3748; margin-bottom: 1rem;">🔬 Data Explorer Dashboard</h2>
        <p style="color: #4a5568; font-size: 1.1rem;">Dive deep into the iris dataset with interactive visualizations</p>
    """, unsafe_allow_html=True)

    # Toggle for raw data with better styling
    show_data = st.checkbox("🗃️ Display Complete Dataset", help="Show the full iris training dataset")
    if show_data:
        st.markdown("### 📊 Complete Iris Dataset")
        st.dataframe(
            df, 
            use_container_width=True,
            height=350
        )

    # Enhanced visualization section
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📈 Feature Distribution Analysis")
        hist_feature = st.selectbox("🌿 Select Feature", feature_names, key="hist_select")
        bins = st.slider("📊 Histogram Resolution", 10, 50, 25, key="bins_slider")
        
        fig_h = px.histogram(
            df, 
            x=hist_feature, 
            nbins=bins, 
            color=df["target"].astype(str),
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'],
            title=f'Distribution: {hist_feature.replace("_", " ").title()}',
            opacity=0.8
        )
        
        fig_h.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255, 255, 255, 0.1)',
            font=dict(color='#2d3748', family='Inter'),
            title_font=dict(size=18, color='#2d3748', family='Poppins'),
            legend_title="Species",
            height=400
        )
        
        st.plotly_chart(fig_h, use_container_width=True)

    with col2:
        st.markdown("### 🎯 Feature Correlation Plot")
        x_feature = st.selectbox("📏 X-Axis Feature", feature_names, index=0, key="x_select")
        y_feature = st.selectbox("📐 Y-Axis Feature", feature_names, index=1, key="y_select")
        
        fig_s = px.scatter(
            df,
            x=x_feature,
            y=y_feature,
            color=df["target"].astype(str),
            color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'],
            title=f'{x_feature.replace("_", " ").title()} vs {y_feature.replace("_", " ").title()}',
            size_max=15,
            opacity=0.8
        )
        
        fig_s.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255, 255, 255, 0.1)',
            font=dict(color='#2d3748', family='Inter'),
            title_font=dict(size=18, color='#2d3748', family='Poppins'),
            legend_title="Species",
            height=400
        )
        
        fig_s.update_traces(marker=dict(size=10, line=dict(width=2, color='white')))
        
        st.plotly_chart(fig_s, use_container_width=True)

    # Enhanced 3D visualization
    st.markdown("### 🌌 Multi-Dimensional Feature Space")
    
    feature_cols = st.columns(3)
    with feature_cols[0]:
        x_3d = st.selectbox("🔴 X Dimension", feature_names, index=0, key="3d_x")
    with feature_cols[1]:
        y_3d = st.selectbox("🟢 Y Dimension", feature_names, index=1, key="3d_y")
    with feature_cols[2]:
        z_3d = st.selectbox("🔵 Z Dimension", feature_names, index=2, key="3d_z")
    
    fig_3d = px.scatter_3d(
        df,
        x=x_3d,
        y=y_3d,
        z=z_3d,
        color=df["target"].astype(str),
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'],
        title='Interactive 3D Feature Exploration',
        height=700,
        opacity=0.8
    )
    
    fig_3d.update_layout(
        scene=dict(
            bgcolor='rgba(255, 255, 255, 0.05)',
            xaxis=dict(
                backgroundcolor='rgba(0,0,0,0)', 
                gridcolor='rgba(255, 255, 255, 0.3)',
                title_font=dict(color='#2d3748')
            ),
            yaxis=dict(
                backgroundcolor='rgba(0,0,0,0)', 
                gridcolor='rgba(255, 255, 255, 0.3)',
                title_font=dict(color='#2d3748')
            ),
            zaxis=dict(
                backgroundcolor='rgba(0,0,0,0)', 
                gridcolor='rgba(255, 255, 255, 0.3)',
                title_font=dict(color='#2d3748')
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2d3748', family='Inter'),
        title_font=dict(size=20, color='#2d3748', family='Poppins'),
        legend_title="Species"
    )
    
    fig_3d.update_traces(marker=dict(size=8, line=dict(width=1, color='white')))
    
    st.plotly_chart(fig_3d, use_container_width=True)

    # Statistical summary section
    st.markdown("### 📈 Statistical Summary")
    
    summary_cols = st.columns(2)
    
    with summary_cols[0]:
        st.markdown("#### 🔢 Feature Statistics")
        feature_for_stats = st.selectbox("Select Feature for Statistics", feature_names, key="stats_feature")
        
        stats = df[feature_for_stats].describe()
        
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.25);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            border: 2px solid rgba(255, 255, 255, 0.3);
        ">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; color: #667eea;">{stats['mean']:.2f}</div>
                    <div style="color: #4a5568; font-size: 0.9rem;">Mean</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; color: #764ba2;">{stats['std']:.2f}</div>
                    <div style="color: #4a5568; font-size: 0.9rem;">Std Dev</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; color: #f093fb;">{stats['min']:.2f}</div>
                    <div style="color: #4a5568; font-size: 0.9rem;">Minimum</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.8rem; font-weight: 700; color: #f5576c;">{stats['max']:.2f}</div>
                    <div style="color: #4a5568; font-size: 0.9rem;">Maximum</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with summary_cols[1]:
        st.markdown("#### 🌺 Species Breakdown")
        
        species_stats = df.groupby('target').size()
        total_samples = len(df)
        
        for i, (species_idx, count) in enumerate(species_stats.items()):
            species_name = target_names[species_idx]
            percentage = (count / total_samples) * 100
            colors = ['#667eea', '#764ba2', '#f093fb']
            
            st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.25);
                border-radius: 12px;
                padding: 1rem;
                margin: 0.8rem 0;
                backdrop-filter: blur(10px);
                border-left: 5px solid {colors[i]};
                display: flex;
                justify-content: space-between;
                align-items: center;
            ">
                <div>
                    <div style="font-weight: 600; color: #2d3748; font-size: 1.1rem;">{species_name}</div>
                    <div style="color: #4a5568; font-size: 0.9rem;">{percentage:.1f}% of dataset</div>
                </div>
                <div style="
                    background: {colors[i]};
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    font-weight: 700;
                    font-size: 1.2rem;
                ">
                    {count}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =============== ENHANCED FOOTER ===============
st.markdown("---")
st.markdown("""
<div style="
    margin-top: 4rem; 
    padding: 3rem; 
    text-align: center; 
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(20px);
    border-radius: 24px 24px 0 0;
    border-top: 3px solid rgba(255, 255, 255, 0.3);
">
    <div class="floating-icon" style="font-size: 2.5rem; margin-bottom: 1rem;">🌸</div>
    <h3 style="
        background: linear-gradient(135deg, #2d3748, #4a5568);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif;
    ">Botanical Iris Laboratory</h3>
    <p style="
        color: #4a5568; 
        font-family: 'Inter', sans-serif; 
        font-size: 1rem;
        margin-bottom: 1rem;
    ">
        🧠 Developed by <span style="
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
        ">Dinesh</span> • Powered by Advanced Machine Learning
    </p>
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
        <div style="
            background: rgba(255, 255, 255, 0.2);
            padding: 0.8rem 1.5rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        ">
            <span style="color: #2d3748; font-weight: 600;">🎯 High Accuracy</span>
        </div>
        <div style="
            background: rgba(255, 255, 255, 0.2);
            padding: 0.8rem 1.5rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        ">
            <span style="color: #2d3748; font-weight: 600;">⚡ Real-time Analysis</span>
        </div>
        <div style="
            background: rgba(255, 255, 255, 0.2);
            padding: 0.8rem 1.5rem;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        ">
            <span style="color: #2d3748; font-weight: 600;">🔬 Scientific Precision</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)