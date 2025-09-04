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

def check_loan_eligibility(model, user_data_processed):
    """
    Uses the trained model to check loan eligibility for multiple users.
    """
    predictions = model.predict(user_data_processed)
    
    print("\n--- Loan Eligibility Results ---")
    for i, prediction in enumerate(predictions):
        user_id = user_data_processed.index[i]  # Use the index as a simple identifier
        if prediction == 1:
            print(f"Record {user_id}: Congratulations! This person is eligible for a loan.")
        else:
            print(f"Record {user_id}: We're sorry, this person is not eligible for a loan at this time.")

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

    # Step 3: Get user input from the file and check eligibility
    user_input_df, _ = load_and_preprocess_data('user_input_many.csv')
    
    if user_input_df is None:
        print("Please ensure 'user_input.csv' exists and is correctly formatted.")
        return
    
    # Ensure user data has same columns as training data
    train_features = train_df.drop(columns=[target_column])
    user_features_processed = preprocess_user_data(user_input_df, train_features.columns)
    
    check_loan_eligibility(model, user_features_processed)
    
    print("\n--- Pipeline execution complete ---")

if __name__ == "__main__":
    main()
