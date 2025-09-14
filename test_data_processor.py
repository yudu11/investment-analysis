# test_data_processor.py

import unittest
import pandas as pd
from data_processor import process_data

class TestDataProcessor(unittest.TestCase):

    def test_process_data(self):
        """Test processing and cleaning data."""
        # Mock data
        gold_data = pd.DataFrame({
            "Date": ["2024-09-14", "2024-09-13", None],
            "Price": [1900.0, 1895.0, None]
        })

        tesla_data = pd.DataFrame({
            "Date": ["2024-09-14", "2024-09-13"],
            "Open": [250.0, None],
            "Close": [260.0, 265.0]
        })

        sp500_data = pd.DataFrame({
            "Date": ["2024-09-14", "2024-09-13"],
            "Open": [4500.0, 4550.0],
            "Close": [4600.0, None]
        })

        dataframes = {
            "gold": gold_data,
            "tesla": tesla_data,
            "sp500": sp500_data
        }

        # Process data
        cleaned_data = process_data(dataframes)

        # Assertions
        self.assertEqual(len(cleaned_data["gold"]), 2)
        self.assertEqual(len(cleaned_data["tesla"]), 1)
        self.assertEqual(len(cleaned_data["sp500"]), 1)

        for name, df in cleaned_data.items():
            self.assertTrue(df.isnull().sum().sum() == 0)  # No missing values

if __name__ == "__main__":
    unittest.main()
