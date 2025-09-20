# Investment Analysis Toolkit

This project automates the collection, cleaning, and visualization of commodity and market data so you can build quick comparisons between gold, Tesla, and the S&P 500. It provides scripts for fetching fresh market data, processing it into clean CSV files, and generating interactive HTML reports.

## Features
- Fetches the latest gold price data from Alpha Vantage (requires an API key).
- Downloads Tesla (`TSLA`) and S&P 500 (`^GSPC`) time series with `yfinance`.
- Cleans and normalizes raw CSV files for downstream analysis.
- Builds timestamped Plotly line charts and saves them to the `output/` directory.

## Environment Setup
1. **Install prerequisites**: Ensure `python3` and `pip` are available on your PATH.
2. **Configure secrets**: Copy `config.json` and update `GOLD_API_KEY` with your Alpha Vantage key. Example:
   ```json
   {
     "GOLD_API_KEY": "YOUR_ALPHA_VANTAGE_KEY"
   }
   ```
3. **Create the virtual environment**:
   ```bash
   bash scripts/setup_venv.sh
   ```
   This script creates `.venv`, upgrades `pip`, and installs dependencies (using `requirements.txt` if present, otherwise installs the core packages directly).
4. **Activate the environment**:
   ```bash
   source scripts/activate_venv.sh
   ```

## Usage
Follow these steps each time you want to refresh data and regenerate the report:

1. **Fetch raw market data**:
   ```bash
   python data_fetcher_runner.py
   ```
   - Saves new CSVs in the `output/` directory: `gold_price_data.csv`, `tesla_stock_price_data.csv`, `sp500_index_data.csv`.
   - Provide `--output-dir path/to/folder` to target a different location.
2. **Process and clean the datasets**:
   ```bash
   python data_processor.py
   ```
   - Reads the raw CSVs from `output/` (or your custom directory) and writes cleaned files alongside them.
   - Accepts `--output-dir` to match the location used in the previous step.
3. **Generate interactive charts**:
   ```bash
   python chart_visualizer.py
   ```
   - Produces timestamped HTML reports in `output/` (for example, `output/gold_20250914_195247.html`) and opens them in your default browser.
   - Use `--output-dir` if your cleaned CSVs live elsewhere.

### Custom Output Directory Example
To keep artifacts in a separate folder (e.g., `artifacts/markets`), append `--output-dir` to each command:
```bash
python data_fetcher_runner.py --output-dir artifacts/markets
python data_processor.py --output-dir artifacts/markets
python chart_visualizer.py --output-dir artifacts/markets
```

## Running Tests
To run the built-in unit tests while the virtual environment is active:
```bash
python -m unittest discover
```

## Project Structure
```
.
├── data_fetcher.py          # Pulls gold, Tesla, and S&P data from APIs
├── data_fetcher_runner.py   # CLI helper to fetch and save the raw CSVs
├── data_processor.py        # Cleans raw datasets and writes normalized CSVs
├── chart_visualizer.py      # Builds Plotly line charts for each dataset
├── scripts/
│   ├── setup_venv.sh        # Creates and provisions the .venv environment
│   └── activate_venv.sh     # Activates the .venv virtual environment
├── output/                  # Destination for generated HTML reports
├── test_data_fetcher.py     # Unit tests validating data_fetcher.py
└── test_data_processor.py   # Unit tests covering the cleaning pipeline
```

## Troubleshooting
- **Missing API key**: `data_fetcher_runner.py` exits if `GOLD_API_KEY` is absent in `config.json`.
- **Stale dependencies**: Re-run `bash scripts/setup_venv.sh` after adding libraries to `requirements.txt`.
- **Charts not opening**: Check the console output for the path; open the HTML report manually from the `output/` directory if the browser does not launch automatically.
