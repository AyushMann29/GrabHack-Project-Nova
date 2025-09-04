import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

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
    """
    y_pred = model.predict(X_test)
    
    print("\n--- Model Evaluation ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(f"Precision: {precision_score(y_test, y_pred):.2f}")
    print(f"Recall: {recall_score(y_test, y_pred):.2f}")
    print(f"F1-Score: {f1_score(y_test, y_pred):.2f}")

def get_user_input():
    """
    Prompts the user for their data in the terminal.
    """
    print("\nPlease enter your data to check for loan eligibility.")
    data = {}
    data['Partner Type'] = input("Enter Partner Type (Driver or Merchant): ")
    data['Earnings (Value)'] = float(input("Enter Earnings (Value): "))
    data['Earnings (Stability Type)'] = input("Enter Earnings (Stability Type): ")
    data['Perf. Rating (Avg)'] = float(input("Enter Performance Rating (Avg): "))
    data['Time on Platform (Months)'] = float(input("Enter Time on Platform (Months): "))
    data['Order/Trip Volume'] = float(input("Enter Order/Trip Volume: "))
    data['Financial Activity (Score)'] = float(input("Enter Financial Activity (Score): "))
    data['Earnings Volatility'] = float(input("Enter Earnings Volatility: "))
    data['On-Time Loan Repayments'] = float(input("Enter On-Time Loan Repayments: "))
    data['Operational Anomaly Score'] = float(input("Enter Operational Anomaly Score: "))
    
    return pd.DataFrame([data])

def preprocess_user_data(user_df, train_columns):
    """
    Prepares the user's data to match the format of the training data.
    """
    categorical_cols = user_df.select_dtypes(include=['object']).columns.tolist()
    user_df = pd.get_dummies(user_df, columns=categorical_cols, drop_first=True)
    
    # Add any missing columns from the training data
    missing_cols = set(train_columns) - set(user_df.columns)
    for c in missing_cols:
        user_df[c] = 0
    
    # Reorder columns to match the training data
    user_df = user_df[train_columns]
    
    return user_df

def check_loan_eligibility(model, user_data):
    """
    Uses the trained model to check loan eligibility.
    """
    prediction = model.predict(user_data)
    if prediction[0] == 1:
        print("\nCongratulations! You are eligible for a loan.")
    else:
        print("\nWe're sorry, you are not eligible for a loan at this time.")

def main():
    """
    Orchestrates the entire pipeline.
    """
    print("--- Starting the Loan Eligibility Checker ---")
    
    # Step 1: Data Loading and Preprocessing
    # Ensure catalyst_train.csv exists before running
    train_df, target_column = load_and_preprocess_data('catalyst_train.csv')
    
    if train_df is None:
        print("Please run the 'generate_datasets.py' script first to create the training data.")
        return
        
    # Step 2: Model Training
    # No need to evaluate the model on the test set if we're just checking user input
    model, _, _ = train_model(train_df, target_column)
    
    # Step 3: Get user input and check eligibility
    user_input_df = get_user_input()
    
    # Ensure user data has same columns as training data
    train_features = train_df.drop(columns=[target_column])
    user_features_processed = preprocess_user_data(user_input_df, train_features.columns)
    
    check_loan_eligibility(model, user_features_processed)
    
    print("\n--- Pipeline execution complete ---")

if __name__ == "__main__":
    main()
