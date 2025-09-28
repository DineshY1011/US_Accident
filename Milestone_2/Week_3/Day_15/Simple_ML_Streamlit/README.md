# 🌸 Iris Classifier – Streamlit + ML Web App

This project is a **Streamlit web app** that trains a machine learning model on the Iris dataset, saves the trained model and metadata, and provides an interactive dashboard for:

- 🌼 **Prediction** – Input flower measurements via sliders and predict the Iris species.
- 📊 **Data Exploration** – Explore histograms, scatter plots, and the raw dataset.

---

## 📂 Project Structure

```
iris_streamlit/
├─ data/
│   └─ iris.csv              # Saved dataset
├─ models/
│   ├─ iris_pipeline.joblib  # Trained ML pipeline
│   └─ feature_stats.json    # Metadata for sliders/UI
├─ train_model.py            # Script to train and save model + metadata
├─ app.py (or ml_app.py)     # Streamlit web app
├─ requirements.txt          # Dependencies
└─ README.md                 # Project guide
```

---

## 🛠️ Installation & Setup

### 1. Clone or create project folder

```bash
mkdir iris_streamlit
cd iris_streamlit
```

### 2. Create virtual environment

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Train the model
This generates:
- `models/iris_pipeline.joblib` (trained pipeline)
- `models/feature_stats.json` (feature stats for sliders)
- `data/iris.csv` (raw dataset)

```bash
python train_model.py
```

### 2. Run the Streamlit app
```bash
streamlit run app.py
```
Open the app in your browser:
👉 http://localhost:8501

---

## 🎯 Features

### Prediction Mode
- Adjust sliders for sepal/petal length & width.
- Get predicted Iris species + confidence score.
- View probability bar chart.

### Data Exploration Mode
- Show raw dataset (`iris.csv`).
- Interactive histogram with adjustable bins.
- Scatter plots to explore feature relationships.

---

## 🧑‍💻 Tech Stack
- Python 3
- Streamlit
- scikit-learn
- pandas
- numpy
- plotly

---

## 🛠️ Troubleshooting
- **ModuleNotFoundError** → Ensure venv is activated and dependencies installed.
- **st.cache deprecation warning** → Already fixed in code with `st.cache_resource` / `st.cache_data`.
- **Port already in use** → Run Streamlit on another port:

```bash
streamlit run app.py --server.port 8502
```