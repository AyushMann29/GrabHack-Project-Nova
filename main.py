from fairlearn.metrics import MetricFrame, selection_rate, true_positive_rate
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import precision_score, recall_score, f1_score
from io import StringIO
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ===============================================================================
# Input Validation Functions
# ===============================================================================
def validate_input(data, trips_col='Number of Trips', earnings_col='Earnings', min_trips=0, max_trips=1000, min_earnings=0, max_earnings=100000):
    """
    Validates input data for negative trips and unrealistic earnings.
    Returns (True, None) if valid, else (False, error_message).
    """
    # Check for single row (dict or DataFrame)
    if isinstance(data, dict):
        trips = data.get(trips_col, None)
        earnings = data.get(earnings_col, None)
        if trips is not None and (trips < min_trips or trips > max_trips):
            return False, f"Invalid number of trips: {trips}. Must be between {min_trips} and {max_trips}."
        if earnings is not None and (earnings < min_earnings or earnings > max_earnings):
            return False, f"Invalid earnings: {earnings}. Must be between {min_earnings} and {max_earnings}."
    elif isinstance(data, pd.DataFrame):
        if trips_col in data.columns:
            invalid_trips = data[(data[trips_col] < min_trips) | (data[trips_col] > max_trips)]
            if not invalid_trips.empty:
                return False, f"Invalid number of trips in rows: {invalid_trips.index.tolist()}"
        if earnings_col in data.columns:
            invalid_earnings = data[(data[earnings_col] < min_earnings) | (data[earnings_col] > max_earnings)]
            if not invalid_earnings.empty:
                return False, f"Invalid earnings in rows: {invalid_earnings.index.tolist()}"
    return True, None

# ==============================================================================
# Step 1: Initialize Flask App and Model Variables
# ==============================================================================
app = Flask(__name__)
CORS(app)  # Enable CORS to allow the frontend to access this API

# Global variables to hold the trained model and features
model = None
train_features_columns = None
evaluation_metrics = {}

# ==============================================================================
# Step 2: Core ML Functions (from your original script)
# ==============================================================================
def load_and_preprocess_data(csv_path):
    """
    Loads and preprocesses the dataset.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: The file {csv_path} was not found.")
        return None, None

    target_column = 'Creditworthy'

    # Drop columns that are not features for the model
    df = df.drop(columns=['Partner ID'], errors='ignore')

    # Identify non-numeric columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Ensure all remaining feature columns are numeric
    for col in df.columns:
        if col != target_column:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop any rows that now have NaN values after the coercion
    df = df.dropna()

    return df, target_column

def train_model(df, target_column):
    """
    Splits data and trains an XGBoost classifier.
    """
    X = df.drop(target_column, axis=1)
    y = df[target_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = XGBClassifier(eval_metric='logloss')
    model.fit(X_train, y_train)

    return model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    """
    Evaluates the trained model using key metrics.
    Returns the metrics as a dictionary.
    """
    y_pred = model.predict(X_test)
    evaluation_metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred)
    }

    # Fairness metrics using Fairlearn (if sensitive attribute exists)
    sensitive_attr = None
    # Try common sensitive attribute names
    for col in ['gender', 'Gender', 'partner_gender', 'Partner Gender']:
        if col in X_test.columns:
            sensitive_attr = X_test[col]
            break
    if sensitive_attr is not None:
        mf = MetricFrame(metrics={'accuracy': accuracy_score, 'selection_rate': selection_rate},
                         y_true=y_test,
                         y_pred=y_pred,
                         sensitive_features=sensitive_attr)
        print("\nFairness metrics by group (Fairlearn):")
        print(mf.by_group)
    else:
        print("No sensitive attribute found for group fairness metrics.")
    return evaluation_metrics

def preprocess_user_data(user_df, train_columns):
    """
    Prepares the user's data to match the format of the training data.
    """
    # Identify and one-hot encode categorical features from the user's data
    categorical_cols = user_df.select_dtypes(include=['object']).columns.tolist()
    user_df = pd.get_dummies(user_df, columns=categorical_cols, drop_first=True)

    # Identify which columns are in the training data but not the user data
    missing_cols = set(train_columns) - set(user_df.columns)

    # Add any missing columns from the training data with default value 0
    for c in missing_cols:
        user_df[c] = 0

    # Drop any extra columns from the user data that were not in the training data
    # This is crucial for single-entry data
    extra_cols = set(user_df.columns) - set(train_columns)
    user_df = user_df.drop(columns=list(extra_cols), errors='ignore')

    # Reorder columns to match the training data
    user_df = user_df[train_columns]

    return user_df

# ==============================================================================
# Step 2.5: New Function to Save Data to CSV
# ==============================================================================
def save_to_csv(data_df, filename='online_testcases.csv'):
    """
    Saves a DataFrame to a CSV file.
    Removes any empty columns (like 'Creditworthy') before saving.
    """
    # Drop 'Creditworthy' if it exists and is empty or all NaN
    if 'Creditworthy' in data_df.columns and data_df['Creditworthy'].isnull().all():
        data_df = data_df.drop(columns=['Creditworthy'])
    # Drop any other columns that are all NaN
    data_df = data_df.dropna(axis=1, how='all')
    file_exists = os.path.isfile(filename)
    data_df.to_csv(filename, mode='a', header=not file_exists, index=False)
    print(f"Data successfully saved to {filename}")

# ==============================================================================
# Step 3: API Endpoint for Prediction (Single Input)
# ==============================================================================
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to receive a single user input, make a prediction, and return metrics.
    """
    # Check if global variables are None. This is the correct way to handle this.
    if model is None or train_features_columns is None or evaluation_metrics is None:
        return jsonify({'error': 'Model is not trained or loaded. Please check backend logs.'}), 500

    try:
        user_input = request.json
        # Input validation
        valid, error_msg = validate_input(user_input)
        if not valid:
            return jsonify({'error': error_msg}), 400

        user_df = pd.DataFrame([user_input])
        # Preprocess the user's data to match the training data format
        user_features_processed = preprocess_user_data(user_df.copy(), train_features_columns)
        # Make the prediction
        prediction = model.predict(user_features_processed)
        result = "Eligible" if prediction[0] == 1 else "Not Eligible"
        # Add prediction to the original DataFrame for logging
        user_df['Creditworthy_Prediction'] = result
        # Save the original user input plus prediction to the CSV file
        save_to_csv(user_df)
        # Return the prediction and evaluation metrics
        return jsonify({
            'prediction': result,
            'metrics': evaluation_metrics
        })

    except Exception as e:
        # Gracefully handle any errors during the process
        return jsonify({'error': str(e)}), 500

# ==============================================================================
# Step 4: API Endpoint for Bulk Prediction (CSV Upload)
# ==============================================================================
@app.route('/predict_csv', methods=['POST'])
def predict_csv():
    """
    Endpoint to receive a CSV file, make bulk predictions, and return results.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Read the CSV file from the request
            csv_data = StringIO(file.read().decode('utf-8'))
            input_df = pd.read_csv(csv_data)

            # Check if ground truth is present
            has_ground_truth = 'Creditworthy' in input_df.columns

            # Remove 'Creditworthy' column from features for prediction
            if has_ground_truth:
                y_true = input_df['Creditworthy']
                input_df_features = input_df.drop(columns=['Creditworthy'])
            else:
                input_df_features = input_df

            # Remove any other empty columns
            input_df_features = input_df_features.dropna(axis=1, how='all')

            # Input validation for all rows
            valid, error_msg = validate_input(input_df_features)
            if not valid:
                return jsonify({'error': error_msg}), 400

            # Preprocess the entire DataFrame
            user_features_processed = preprocess_user_data(input_df_features.copy(), train_features_columns)
            # Make the predictions
            predictions = model.predict(user_features_processed)
            # Add the predictions to the original DataFrame
            input_df['Creditworthy_Prediction'] = np.where(predictions == 1, 'Eligible', 'Not Eligible')

            # Remove any empty columns again before saving/returning
            input_df = input_df.dropna(axis=1, how='all')

            # Save the entire DataFrame to the CSV file
            save_to_csv(input_df)

            # --- Fairness & Bias Reporting ---
            fairness_metrics = {}
            fairness_observation = "Fairness metrics require ground truth labels and are not available for this upload."
            if has_ground_truth:
                # Only compute fairness if ground truth is present
                sensitive_col = 'Partner Type'
                if sensitive_col in input_df.columns:
                    y_pred = (input_df['Creditworthy_Prediction'] == 'Eligible').astype(int)
                    # If Creditworthy is string, convert to binary
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
                    # Observations
                    rates = mf.by_group['selection_rate']
                    max_group = rates.idxmax()
                    min_group = rates.idxmin()
                    diff = rates[max_group] - rates[min_group]
                    fairness_observation = f"{max_group} group approval rate is {diff:.2%} higher than {min_group} group."
                    if abs(diff) > 0.1:
                        fairness_observation += " Mitigation recommended: Consider reweighting or post-processing."

            # Convert DataFrame to a list of dictionaries for JSON response
            results = input_df.to_dict('records')
            return jsonify({
                'predictions': results,
                'metrics': evaluation_metrics,
                'fairness_metrics': fairness_metrics,
                'fairness_observation': fairness_observation
            })
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return jsonify({'error': f"Error processing file: {str(e)}"}), 500

    return jsonify({'error': 'An unknown error occurred.'}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Endpoint to receive user feedback and send an email.
    """
    try:
        EMAIL_FROM = os.environ.get("EMAIL_FROM")
        EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
        EMAIL_TO = os.environ.get("EMAIL_TO")
        SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))

        data = request.json or {}
        name = data.get('name', 'Anonymous')
        email = data.get('email', 'No email provided')
        rating = data.get('rating', 'No rating provided')
        message = data.get('message', 'No message provided')

        # Compose email
        subject = f"New Feedback from {name}"
        body = f"""
        You have received new feedback:

        Name: {name}
        Email: {email}
        Rating: {rating}
        Message: {message}
        """

        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "Feedback sent successfully!"}), 200
    
    except Exception as e:
        import traceback
        print("Error sending feedback email:", e)
        traceback.print_exc()
        return jsonify({"error": "Failed to send feedback"}), 500


# ==============================================================================
# Step 5: Main function to train the model once and run the server
# ==============================================================================
def main():
    """
    Initializes the model and runs the Flask server.
    """
    global model, train_features_columns, evaluation_metrics

    print("--- Starting the Nova Backend ---")
    print("Step 1: Loading and preprocessing data...")
    train_df, target_column = load_and_preprocess_data('catalyst_train.csv')

    if train_df is None:
        print("Please ensure 'catalyst_train.csv' exists. Exiting.")
        return

    print("Step 2: Training the model and evaluating performance...")
    model, X_test, y_test = train_model(train_df, target_column)
    train_features_columns = train_df.drop(columns=[target_column]).columns
    evaluation_metrics = evaluate_model(model, X_test, y_test)

    print("\nModel trained successfully! Metrics:")
    for key, value in evaluation_metrics.items():
        print(f"- {key.capitalize()}: {value:.4f}")

    print("\n--- Starting Flask server on http://127.0.0.1:5000 ---")
    # This will serve the API, ready to accept requests from the frontend
    app.run(debug=True, port=5000, use_reloader=False)

if __name__ == "__main__":
    main()
