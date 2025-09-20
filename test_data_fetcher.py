# test_data_fetcher.py

import unittest
from unittest.mock import patch, MagicMock
import data_fetcher
import pandas as pd

class TestDataFetcher(unittest.TestCase):

    @patch("data_fetcher.requests.get")
    def test_fetch_gold_price_success(self, mock_get):
        """Test fetching gold price data successfully."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Time Series (Daily)": {
                "2025-09-13": {
                    "1. open": "1900.0",
                    "2. high": "1910.0",
                    "3. low": "1890.0",
                    "4. close": "1905.0",
                    "5. volume": "1000"
                },
                "2025-09-12": {
                    "1. open": "1895.0",
                    "2. high": "1905.0",
                    "3. low": "1885.0",
                    "4. close": "1890.0",
                    "5. volume": "1200"
                }
            }
        }
        mock_get.return_value = mock_response

        # Call the function
        api_key = "test_key"
        result = data_fetcher.fetch_gold_price(api_key)

        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn("Date", result.columns)
        self.assertIn("open", result.columns)
        self.assertIn("high", result.columns)
        self.assertIn("low", result.columns)
        self.assertIn("close", result.columns)
        self.assertIn("volume", result.columns)

    @patch("data_fetcher.requests.get")
    def test_fetch_gold_price_failure(self, mock_get):
        """Test fetching gold price data with API failure."""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        # Call the function and assert exception
        api_key = "test_key"
        with self.assertRaises(Exception) as context:
            data_fetcher.fetch_gold_price(api_key)

        self.assertIn("Failed to fetch gold price data", str(context.exception))

    @patch("data_fetcher.yf.download")
    def test_fetch_tesla_stock_price_success(self, mock_download):
        """Test fetching Tesla stock price data successfully."""
        # Mock yfinance response
        mock_data = pd.DataFrame({
            "Date": ["2024-09-14", "2024-09-13"],
            "Open": [250.0, 255.0],
            "Close": [260.0, 265.0]
        })
        mock_download.return_value = mock_data

        # Call the function
        result = data_fetcher.fetch_tesla_stock_price()

        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn("Date", result.columns)
        self.assertIn("Open", result.columns)
        self.assertIn("Close", result.columns)

    @patch("data_fetcher.yf.download")
    def test_fetch_sp500_index_success(self, mock_download):
        """Test fetching S&P500 index data successfully."""
        # Mock yfinance response
        mock_data = pd.DataFrame({
            "Date": ["2024-09-14", "2024-09-13"],
            "Open": [4500.0, 4550.0],
            "Close": [4600.0, 4650.0]
        })
        mock_download.return_value = mock_data

        # Call the function
        result = data_fetcher.fetch_sp500_index()

        # Assertions
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertIn("Date", result.columns)
        self.assertIn("Open", result.columns)
        self.assertIn("Close", result.columns)

if __name__ == "__main__":
    unittest.main()
