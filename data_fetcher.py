# data_fetcher.py

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import requests
import yfinance as yf

def fetch_gold_price(api_key):
    """
    Fetch the past 1 year's daily gold price data using Alpha Vantage API.

    Args:
        api_key (str): API key for authentication.

    Returns:
        pd.DataFrame: DataFrame containing the gold price data.
    """
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # Daily time series
        "symbol": "XAUUSD",  # Symbol for gold price in USD
        "outputsize": "full",  # Fetch full data to ensure we get 1 year
        "datatype": "json",  # Get data in JSON format
        "apikey": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Debug: API Response Data", data)  # Debug statement
        if "Time Series (Daily)" in data:
            # Extract relevant fields
            time_series = data["Time Series (Daily)"]
            print("Debug: Time Series (Daily)", time_series)  # Debug statement
            df = pd.DataFrame.from_dict(time_series, orient="index")
            df = df.rename(columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. volume": "volume"
            })
            print("Debug: DataFrame after renaming columns", df.head())  # Debug statement
            df.index = pd.to_datetime(df.index)
            df = df[df.index >= (datetime.now() - timedelta(days=365))]  # Filter past 1 year
            df = df.sort_index()  # Sort by date
            df.reset_index(inplace=True)  # Ensure 'Date' is a column
            df.rename(columns={"index": "Date"}, inplace=True)  # Rename index to 'Date'
            print("Debug: Final DataFrame", df.head())  # Debug statement
            return df
        else:
            raise Exception("Unexpected response format: Missing 'Time Series (Daily)'")
    else:
        raise Exception(f"Failed to fetch gold price data: {response.status_code}, {response.text}")

def fetch_tesla_stock_price():
    """
    Fetch the past 1 year's Tesla stock price data using yfinance.

    Returns:
        pd.DataFrame: DataFrame containing Tesla stock price data.
    """
    # Define the ticker symbol for Tesla
    ticker = "TSLA"

    # Fetch data for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    tesla_data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))

    # Reset index to make 'Date' a column
    tesla_data.reset_index(inplace=True)

    return tesla_data

def fetch_sp500_index():
    """
    Fetch the past 1 year's S&P500 index data using yfinance.

    Returns:
        pd.DataFrame: DataFrame containing S&P500 index data.
    """
    # Define the ticker symbol for S&P500
    ticker = "^GSPC"

    # Fetch data for the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    sp500_data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))

    # Reset index to make 'Date' a column
    sp500_data.reset_index(inplace=True)

    return sp500_data

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch market data and write it to CSV files.")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where CSV files will be saved (default: output)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = Path(__file__).resolve().parent / "config.json"
    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    api_key_gold = config.get("GOLD_API_KEY")

    if not api_key_gold:
        raise EnvironmentError("Please set the GOLD_API_KEY in config.json.")

    try:
        # Fetch and save gold price data
        gold_data = fetch_gold_price(api_key_gold)
        gold_path = output_dir / "gold_price_data.csv"
        gold_data.to_csv(gold_path, index=False)
        print(f"Gold price data saved to {gold_path}")
    except Exception as e:
        print(f"Error fetching gold price data: {e}")

    try:
        # Fetch Tesla stock price data
        tesla_data = fetch_tesla_stock_price()
        tesla_path = output_dir / "tesla_stock_price_data.csv"
        tesla_data.to_csv(tesla_path, index=False)
        print(f"Tesla stock price data saved to {tesla_path}")
    except Exception as e:
        print(f"Error fetching Tesla stock price data: {e}")

    try:
        # Fetch S&P500 index data
        sp500_data = fetch_sp500_index()
        sp500_path = output_dir / "sp500_index_data.csv"
        sp500_data.to_csv(sp500_path, index=False)
        print(f"S&P500 index data saved to {sp500_path}")
    except Exception as e:
        print(f"Error fetching S&P500 index data: {e}")
