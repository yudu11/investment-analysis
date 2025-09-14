# data_fetcher.py

import requests
import os
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import json

def fetch_gold_price(api_key):
    """
    Fetch the past 1 year's gold price data using Alpha Vantage API.

    Args:
        api_key (str): API key for authentication.

    Returns:
        pd.DataFrame: DataFrame containing the gold price data.
    """
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_WEEKLY_ADJUSTED",  # Weekly adjusted time series
        "symbol": "XAUUSD",  # Symbol for gold price in USD
        "apikey": api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print("API Response:", response.json())  # Log the full API response for debugging
        if "Weekly Adjusted Time Series" in data:
            # Extract relevant fields
            time_series = data["Weekly Adjusted Time Series"]
            df = pd.DataFrame.from_dict(time_series, orient="index")
            df = df.rename(columns={
                "1. open": "open",
                "2. high": "high",
                "3. low": "low",
                "4. close": "close",
                "5. adjusted close": "adjusted_close",
                "6. volume": "volume",
                "7. dividend amount": "dividend_amount"
            })
            df.index = pd.to_datetime(df.index)
            df = df[df.index >= (datetime.now() - timedelta(days=365))]  # Filter past 1 year
            df = df.sort_index()  # Sort by date
            df.reset_index(inplace=True)  # Ensure 'Date' is a column
            df.rename(columns={"index": "Date"}, inplace=True)  # Rename index to 'Date'
            return df
        else:
            raise Exception("Unexpected response format: Missing 'Weekly Adjusted Time Series'")
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
    start_date = end_date - timedelta(days=365)

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
    start_date = end_date - timedelta(days=365)

    sp500_data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))

    # Reset index to make 'Date' a column
    sp500_data.reset_index(inplace=True)

    return sp500_data

if __name__ == "__main__":
    # Load API keys from config.json
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    api_key_gold = config.get("GOLD_API_KEY")
    api_key_tesla = config.get("TESLA_API_KEY")
    api_key_sp500 = config.get("SP500_API_KEY")

    if not api_key_gold:
        raise EnvironmentError("Please set the GOLD_API_KEY in config.json.")
    if not api_key_tesla:
        raise EnvironmentError("Please set the TESLA_API_KEY in config.json.")
    if not api_key_sp500:
        raise EnvironmentError("Please set the SP500_API_KEY in config.json.")

    try:
        gold_data = fetch_gold_price(api_key_gold)
        gold_data.to_csv("gold_price_data.csv", index=False)
        print("Gold price data saved to gold_price_data.csv")
    except Exception as e:
        print(f"Error: {e}")
