from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from io import StringIO
import os

# Load model and columns
MODEL_PATH = "xgboost_credit_model.joblib"
COLS_PATH = "train_features_columns.joblib"
METRICS_PATH = "evaluation_metrics.joblib"

model = joblib.load(MODEL_PATH)
train_features_columns = joblib.load(COLS_PATH)
if os.path.exists(METRICS_PATH):
    evaluation_metrics = joblib.load(METRICS_PATH)
else:
    evaluation_metrics = {}

app = Flask(__name__)
CORS(app)

def preprocess_user_data(user_df, train_columns):
    # One-hot encode categorical columns
    categorical_cols = user_df.select_dtypes(include=['object']).columns.tolist()
    user_df = pd.get_dummies(user_df, columns=categorical_cols, drop_first=True)
    # Add missing columns
    missing_cols = set(train_columns) - set(user_df.columns)
    for c in missing_cols:
        user_df[c] = 0
    # Remove extra columns
    extra_cols = set(user_df.columns) - set(train_columns)
    user_df = user_df.drop(columns=list(extra_cols), errors='ignore')
    # Reorder
    user_df = user_df[train_columns]
    return user_df

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_input = request.json
        user_df = pd.DataFrame([user_input])
        user_features_processed = preprocess_user_data(user_df.copy(), train_features_columns)
        prediction = model.predict(user_features_processed)
        result = "Eligible" if prediction[0] == 1 else "Not Eligible"
        return jsonify({
            'prediction': result,
            'metrics': evaluation_metrics
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_csv', methods=['POST'])
def predict_csv():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        csv_data = StringIO(file.read().decode('utf-8'))
        input_df = pd.read_csv(csv_data)
        # Remove Creditworthy if present
        if 'Creditworthy' in input_df.columns:
            input_df = input_df.drop(columns=['Creditworthy'])
        input_df = input_df.dropna(axis=1, how='all')
        user_features_processed = preprocess_user_data(input_df.copy(), train_features_columns)
        predictions = model.predict(user_features_processed)
        input_df['Creditworthy_Prediction'] = np.where(predictions == 1, 'Eligible', 'Not Eligible')
        results = input_df.to_dict('records')
        return jsonify({
            'predictions': results,
            'metrics': evaluation_metrics,
            'fairness_metrics': {},
            'fairness_observation': "Fairness metrics require ground truth labels and are not available for this upload."
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)