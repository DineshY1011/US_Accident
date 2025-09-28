# train_model.py
import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# 1) Ensure folders exist
os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)

# 2) Load Iris dataset
iris = load_iris()
X = iris.data                  # shape (150,4)
y = iris.target                # integer labels 0,1,2
feature_names = iris.feature_names  # e.g., ['sepal length (cm)', ...]
target_names = iris.target_names.tolist()  # ['setosa', 'versicolor', 'virginica']

# 3) Save raw dataset (optional but useful)
df = pd.DataFrame(X, columns=feature_names)
df['target'] = y
df.to_csv("data/iris.csv", index=False)
print("Saved raw dataset to data/iris.csv")

# 4) Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5) Create pipeline (scaler + classifier)
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
])

# 6) Train
pipeline.fit(X_train, y_train)

# 7) Evaluate
y_pred = pipeline.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {acc:.4f}")
print("Classification report:")
print(classification_report(y_test, y_pred, target_names=target_names))

# 8) Save model
model_path = "models/iris_pipeline.joblib"
joblib.dump(pipeline, model_path)
print("Saved model to", model_path)

# 9) Save feature statistics (min,max,mean,std) for UI sliders
feature_stats = {}
for i, fname in enumerate(feature_names):
    col = X[:, i]
    feature_stats[fname] = {
        "min": float(col.min()),
        "max": float(col.max()),
        "mean": float(col.mean()),
        "std": float(col.std())
    }

meta = {
    "feature_stats": feature_stats,
    "feature_names": feature_names,
    "target_names": target_names
}

with open("models/feature_stats.json", "w") as f:
    json.dump(meta, f, indent=2)

print("Saved feature stats to models/feature_stats.json")