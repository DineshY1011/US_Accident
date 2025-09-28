# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
import plotly.express as px

# Page config
st.set_page_config(page_title="Iris Classifier", layout="centered")

st.title("Iris Species Classifier")
st.write("Simple Streamlit app: enter flower measurements and get a predicted Iris species.")

# Helper: load model and metadata
@st.cache_resource
def load_model_and_meta():
    model = joblib.load("models/iris_pipeline.joblib")
    with open("models/feature_stats.json", "r") as f:
        meta = json.load(f)
    df = pd.read_csv("data/iris.csv")
    return model, meta, df

# Load once
model, meta, df = load_model_and_meta()
feature_stats = meta["feature_stats"]
feature_names = meta["feature_names"]
target_names = meta["target_names"]

# Sidebar: choose mode
mode = st.sidebar.radio("Mode", ["Prediction", "Data Exploration"])

if mode == "Prediction":
    st.header("Prediction")
    st.write("Adjust the sliders or input boxes to set measurements for a single flower.")

    # Create inputs in two-column layout
    cols = st.columns(2)
    values = []
    # We keep insertion order of feature_stats dictionary
    for i, fname in enumerate(feature_names):
        stats = feature_stats[fname]
        min_val = stats["min"]
        max_val = stats["max"]
        mean_val = stats["mean"]
        # put alternating sliders into two columns
        if i % 2 == 0:
            val = cols[0].slider(label=fname, min_value=float(min_val), max_value=float(max_val), value=float(mean_val))
        else:
            val = cols[1].slider(label=fname, min_value=float(min_val), max_value=float(max_val), value=float(mean_val))
        values.append(val)

    # Predict button
    if st.button("Predict"):
        X_input = np.array(values).reshape(1, -1)
        pred = model.predict(X_input)[0]
        probs = model.predict_proba(X_input)[0]
        pred_name = target_names[pred]

        st.markdown("### Prediction result")
        # Color-coding based on confidence
        confidence = float(probs[pred])
        if confidence >= 0.75:
            st.success(f"Predicted species: **{pred_name}** (confidence {confidence:.2f})")
        elif confidence >= 0.45:
            st.info(f"Predicted species: **{pred_name}** (confidence {confidence:.2f})")
        else:
            st.warning(f"Low-confidence prediction: **{pred_name}** (confidence {confidence:.2f})")

        # Show probability bar chart
        prob_df = pd.DataFrame({"species": target_names, "probability": list(probs)})
        fig = px.bar(prob_df, x="species", y="probability", range_y=[0, 1], title="Prediction probabilities")
        st.plotly_chart(fig, use_container_width=True)

        # Show raw probabilities in a table
        st.table(prob_df.set_index("species"))

elif mode == "Data Exploration":
    st.header("Data Exploration")
    if st.checkbox("Show raw dataset"):
        st.dataframe(df)

    st.subheader("Histogram")
    hist_feature = st.selectbox("Feature for histogram", feature_names, index=0)
    bins = st.slider("Number of bins", min_value=5, max_value=50, value=15)
    fig_h = px.histogram(df, x=hist_feature, nbins=bins, title=f"Histogram of {hist_feature}")
    st.plotly_chart(fig_h, use_container_width=True)

    st.subheader("Scatter plot (pairwise)")
    x_feature = st.selectbox("X axis", feature_names, index=0, key="x")
    y_feature = st.selectbox("Y axis", feature_names, index=1, key="y")
    color_opt = st.selectbox("Color by", ["target"], index=0)
    fig_s = px.scatter(df, x=x_feature, y=y_feature, color=df["target"].astype(str), title=f"{x_feature} vs {y_feature}")
    st.plotly_chart(fig_s, use_container_width=True)

    st.write("Tip: Use the dropdowns to explore different features and the histogram bins slider to adjust detail.")