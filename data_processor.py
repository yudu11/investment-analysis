# data_processor.py

import pandas as pd

def process_data(dataframes):
    """
    Process and clean the fetched data for visualization.

    Args:
        dataframes (dict): A dictionary where keys are dataset names (e.g., 'gold', 'tesla', 'sp500')
                          and values are the corresponding DataFrames.

    Returns:
        dict: A dictionary of cleaned DataFrames.
    """
    processed_data = {}

    for name, df in dataframes.items():
        # Ensure the 'Date' column is in datetime format
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

        # Drop rows with missing values
        df.dropna(inplace=True)

        # Sort by date
        df.sort_values(by='Date', inplace=True)

        # Store the cleaned DataFrame
        processed_data[name] = df

    return processed_data

if __name__ == "__main__":
    # Example usage
    gold_data = pd.read_csv("gold_price_data.csv")
    tesla_data = pd.read_csv("tesla_stock_data.csv")
    sp500_data = pd.read_csv("sp500_index_data.csv")

    dataframes = {
        "gold": gold_data,
        "tesla": tesla_data,
        "sp500": sp500_data
    }

    cleaned_data = process_data(dataframes)

    for name, df in cleaned_data.items():
        df.to_csv(f"cleaned_{name}_data.csv", index=False)
        print(f"Cleaned {name} data saved to cleaned_{name}_data.csv")
