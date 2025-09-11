import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

# 1. Load and preprocess data
csv_path = 'catalyst_train.csv'
target_column = 'Creditworthy'

df = pd.read_csv(csv_path)
if 'Partner ID' in df.columns:
    df = df.drop(columns=['Partner ID'])

# One-hot encode categorical columns
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
if target_column in categorical_cols:
    categorical_cols.remove(target_column)
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Ensure all columns except target are numeric
for col in df.columns:
    if col != target_column:
        df[col] = pd.to_numeric(df[col], errors='coerce')
df = df.dropna()

# 2. Split and train
X = df.drop(target_column, axis=1)
y = df[target_column]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBClassifier(eval_metric='logloss')
model.fit(X_train, y_train)

# 3. Evaluate
y_pred = model.predict(X_test)
metrics = {
    'accuracy': accuracy_score(y_test, y_pred),
    'precision': precision_score(y_test, y_pred),
    'recall': recall_score(y_test, y_pred),
    'f1_score': f1_score(y_test, y_pred)
}
print("Evaluation metrics:")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")

# 4. Save model and columns
joblib.dump(model, 'xgboost_credit_model.joblib')
joblib.dump(list(X_train.columns), 'train_features_columns.joblib')
joblib.dump(metrics, 'evaluation_metrics.joblib')
print("Artifacts saved: xgboost_credit_model.joblib, train_features_columns.joblib, evaluation_metrics.joblib")