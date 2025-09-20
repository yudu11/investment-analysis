# data_processor.py

import argparse
from pathlib import Path

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

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean raw market datasets and persist normalized CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory containing raw CSVs and where cleaned files will be saved (default: output)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_files = {
        "gold": output_dir / "gold_price_data.csv",
        "tesla": output_dir / "tesla_stock_price_data.csv",
        "sp500": output_dir / "sp500_index_data.csv",
    }

    dataframes = {}
    missing_files = []
    for name, path in input_files.items():
        if path.exists():
            dataframes[name] = pd.read_csv(path)
        else:
            missing_files.append(path)

    if missing_files:
        print("Error: Missing expected input files:")
        for path in missing_files:
            print(f" - {path}")
        exit(1)

    cleaned_data = process_data(dataframes)

    for name, df in cleaned_data.items():
        output_path = output_dir / f"cleaned_{name}_data.csv"
        df.to_csv(output_path, index=False)
        print(f"Cleaned {name} data saved to {output_path}")
