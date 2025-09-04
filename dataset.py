import pandas as pd
import numpy as np

def generate_catalyst_dataset(num_records):
    """
    Generates a synthetic dataset for the Catalyst Score Platform.
    
    Args:
        num_records (int): The number of rows to generate.
    
    Returns:
        pandas.DataFrame: The generated synthetic dataset.
    """
    columns = [
        "Partner ID", "Partner Type", "Earnings (Value)", "Earnings (Stability Type)",
        "Perf. Rating (Avg)", "Time on Platform (Months)", "Order/Trip Volume",
        "Financial Activity (Score)", "Earnings Volatility",
        "On-Time Loan Repayments", "Operational Anomaly Score"
    ]
    df = pd.DataFrame(index=range(num_records), columns=columns)

    df['Partner ID'] = [f'00{i:03d}' for i in range(1, num_records + 1)]
    df['Partner Type'] = np.random.choice(['Driver', 'Merchant'], size=num_records, p=[0.7, 0.3])

    df['Earnings (Value)'] = df['Partner Type'].apply(
        lambda x: np.random.randint(1000, 2500) if x == 'Driver' else np.random.randint(800, 2000)
    )

    df['Earnings (Stability Type)'] = df['Partner Type'].apply(
        lambda x: np.random.choice(['Stable', 'Seasonal', 'Variable'], p=[0.6, 0.2, 0.2])
    )
    
    df['Time on Platform (Months)'] = np.random.randint(1, 48, size=num_records)
    
    df['Perf. Rating (Avg)'] = (
        4.0 + (df['Time on Platform (Months)'] / 48 * 0.9) + np.random.normal(0, 0.2, num_records)
    ).clip(3.0, 5.0).round(1)

    df['Order/Trip Volume'] = (
        df['Earnings (Value)'] * np.random.uniform(0.15, 0.25, num_records) + np.random.randint(50, 200)
    ).astype(int)
    
    df['Financial Activity (Score)'] = (
        (df['Earnings (Value)'] / 2500 * 0.6) + 
        (df['Time on Platform (Months)'] / 48 * 0.3) + 
        np.random.uniform(-0.1, 0.1, num_records)
    ).clip(0, 1).round(2)

    df['Earnings Volatility'] = (
        1 - (df['Earnings (Value)'] / 2500) - np.random.uniform(0, 0.3, num_records)
    ).clip(0.1, 0.9).round(2)

    df['On-Time Loan Repayments'] = (
        df['Financial Activity (Score)'] * 20 + np.random.randint(-2, 3, num_records)
    ).clip(0, 15).astype(int)
    
    df['Operational Anomaly Score'] = (
        1 - (df['Perf. Rating (Avg)'] / 5) + np.random.uniform(-0.1, 0.2, num_records)
    ).clip(0, 1).round(2)
    
    # Calculate the raw score based on the provided formula
    df['Raw Score'] = (
        df['Perf. Rating (Avg)'] * 0.18 +
        df['Financial Activity (Score)'] * 0.28 +
        (df['Time on Platform (Months)'] / 60) * 0.12 +
        (1 - df['Earnings Volatility']) * 0.08 +
        (df['On-Time Loan Repayments'] / 20) * 0.08 +
        (1 - df['Operational Anomaly Score']) * 0.18 +
        np.random.uniform(0, 1) * 0.08 + # Placeholder for 'Engagement Score'
        (df['Earnings (Value)'] / 2500) * 0.05
    )
    
    # Create the binary target variable 'Creditworthy'
    df['Creditworthy'] = (df['Raw Score'] > df['Raw Score'].mean()).astype(int)

    # Drop the intermediate raw score column
    df = df.drop(columns=['Raw Score'])

    return df

# Main logic to generate datasets
if __name__ == '__main__':
    # Generate training, testing, and user datasets with specified sizes
    train_df = generate_catalyst_dataset(num_records=10000)
    test_df = generate_catalyst_dataset(num_records=2000)
    user_df = generate_catalyst_dataset(num_records=1)

    # Save the datasets to CSV files
    train_df.to_csv('catalyst_train.csv', index=False)
    test_df.to_csv('catalyst_test.csv', index=False)
    user_df.to_csv('user_input.csv', index=False)

    print("Datasets created successfully!")
    print(f"Training dataset: catalyst_train.csv ({len(train_df)} rows)")
    print(f"Testing dataset: catalyst_test.csv ({len(test_df)} rows)")
    print(f"User input dataset: user_input.csv ({len(user_df)} rows)")
