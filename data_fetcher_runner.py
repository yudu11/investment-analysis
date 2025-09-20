# data_fetcher_runner.py

import argparse
import json
from pathlib import Path

import data_fetcher


def save_data_to_csv(output_dir: Path) -> None:
    """Fetch data for gold, Tesla, and S&P500, and save them to CSV files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    config_path = Path(__file__).resolve().parent / "config.json"
    with config_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    api_key_gold = config.get("GOLD_API_KEY")
    if not api_key_gold:
        print("Error: Please set the GOLD_API_KEY in config.json.")
        exit(1)

    try:
        # Fetch and save gold price data
        gold_data = data_fetcher.fetch_gold_price(api_key_gold)
        gold_path = output_dir / "gold_price_data.csv"
        gold_data.to_csv(gold_path, index=False)
        print(f"Gold price data saved to {gold_path}")

        # Fetch and save Tesla stock price data
        tesla_data = data_fetcher.fetch_tesla_stock_price()
        tesla_path = output_dir / "tesla_stock_price_data.csv"
        tesla_data.to_csv(tesla_path, index=False)
        print(f"Tesla stock price data saved to {tesla_path}")

        # Fetch and save S&P500 index data
        sp500_data = data_fetcher.fetch_sp500_index()
        sp500_path = output_dir / "sp500_index_data.csv"
        sp500_data.to_csv(sp500_path, index=False)
        print(f"S&P500 index data saved to {sp500_path}")

    except Exception as e:
        print(f"Error: {e}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch market datasets and write them to CSV files.")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where CSV files will be saved (default: output)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    save_data_to_csv(Path(args.output_dir))
