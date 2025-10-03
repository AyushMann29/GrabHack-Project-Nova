import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ----------------------------
# 1. Load training data
# ----------------------------
csv_path = "catalyst_train.csv"
target_column = "Creditworthy"

df = pd.read_csv(csv_path)

# Drop unnecessary column
if "Partner ID" in df.columns:
    df = df.drop(columns=["Partner ID"])

# Identify column types
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()
if target_column in categorical_cols:
    categorical_cols.remove(target_column)
numerical_cols = df.drop(columns=[target_column] + categorical_cols).columns.tolist()

X = df.drop(target_column, axis=1)
y = df[target_column]

# ----------------------------
# 2. Define preprocessing
# ----------------------------
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

# ----------------------------
# 3. Create pipeline
# ----------------------------
pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", XGBClassifier(eval_metric="logloss", use_label_encoder=False))
])

# ----------------------------
# 4. Train-test split & fit
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

# ----------------------------
# 5. Evaluate
# ----------------------------
y_pred = pipeline.predict(X_test)

metrics = {
    "accuracy": accuracy_score(y_test, y_pred),
    "precision": precision_score(y_test, y_pred),
    "recall": recall_score(y_test, y_pred),
    "f1_score": f1_score(y_test, y_pred)
}

print("Evaluation metrics:")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")

# ----------------------------
# 6. Save pipeline + metrics
# ----------------------------
joblib.dump(pipeline, "xgboost_credit_model.joblib")
joblib.dump(metrics, "evaluation_metrics.joblib")

print("Artifacts saved: xgboost_credit_model.joblib, evaluation_metrics.joblib")