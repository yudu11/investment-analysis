# data_fetcher_runner.py

import data_fetcher
import os
import json

def save_data_to_csv():
    """
    Fetch data for gold, Tesla, and S&P500, and save them to CSV files.
    """
    # Load API keys from config.json
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    api_key_gold = config.get("GOLD_API_KEY")
    if not api_key_gold:
        print("Error: Please set the GOLD_API_KEY in config.json.")
        exit(1)

    try:
        # Fetch and save gold price data
        gold_data = data_fetcher.fetch_gold_price(api_key_gold)
        gold_data.to_csv("gold_price_data.csv", index=False)
        print("Gold price data saved to gold_price_data.csv")

        # Fetch and save Tesla stock price data
        tesla_data = data_fetcher.fetch_tesla_stock_price()
        tesla_data.to_csv("tesla_stock_data.csv", index=False)
        print("Tesla stock price data saved to tesla_stock_data.csv")

        # Fetch and save S&P500 index data
        sp500_data = data_fetcher.fetch_sp500_index()
        sp500_data.to_csv("sp500_index_data.csv", index=False)
        print("S&P500 index data saved to sp500_index_data.csv")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    save_data_to_csv()
