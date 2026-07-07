from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from io import StringIO
import os
from fairlearn.metrics import MetricFrame, selection_rate, true_positive_rate
from sklearn.metrics import accuracy_score

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

@app.route('/')
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'Nova API'})

def preprocess_user_data(user_df, train_columns):
    missing_cols = set(train_columns) - set(user_df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
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
        input_df = pd.read_csv(csv_data, low_memory=False, engine='c')

        has_ground_truth = 'Creditworthy' in input_df.columns
        if has_ground_truth:
            y_true = input_df['Creditworthy']
            input_df_features = input_df.drop(columns=['Creditworthy'])
        else:
            input_df_features = input_df

        input_df_features = input_df_features.dropna(axis=1, how='all')
        user_features_processed = preprocess_user_data(input_df_features.copy(), train_features_columns)
        predictions = model.predict(user_features_processed)
        input_df['Creditworthy_Prediction'] = np.where(predictions == 1, 'Eligible', 'Not Eligible')

        fairness_metrics = {}
        fairness_observation = "Fairness metrics require ground truth labels and are not available for this upload."
        if has_ground_truth:
            sensitive_col = 'Partner Type'
            if sensitive_col in input_df.columns:
                y_pred = (input_df['Creditworthy_Prediction'] == 'Eligible').astype(int)
                if y_true.dtype == object:
                    y_true_bin = y_true.map(lambda x: 1 if str(x).lower() in ['eligible', '1', 'true', 'yes'] else 0)
                else:
                    y_true_bin = y_true
                sensitive_features = input_df[sensitive_col]
                mf = MetricFrame(
                    metrics={
                        'selection_rate': selection_rate,
                        'equal_opportunity': true_positive_rate
                    },
                    y_true=y_true_bin,
                    y_pred=y_pred,
                    sensitive_features=sensitive_features
                )
                fairness_metrics = {
                    'selection_rate': mf.by_group['selection_rate'].to_dict(),
                    'equal_opportunity': mf.by_group['equal_opportunity'].to_dict()
                }
                rates = mf.by_group['selection_rate']
                max_group = rates.idxmax()
                min_group = rates.idxmin()
                diff = rates[max_group] - rates[min_group]
                fairness_observation = f"{max_group} group approval rate is {diff:.2%} higher than {min_group} group."
                if abs(diff) > 0.1:
                    fairness_observation += " Mitigation recommended: Consider reweighting or post-processing."

        results = input_df.to_dict('records')
        return jsonify({
            'predictions': results,
            'metrics': evaluation_metrics,
            'fairness_metrics': fairness_metrics,
            'fairness_observation': fairness_observation
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        return jsonify({'message': 'Feedback received', 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)