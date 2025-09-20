# chart_visualizer.py

import argparse
from datetime import datetime
from pathlib import Path
import webbrowser

import pandas as pd
import plotly.graph_objects as go


def create_individual_charts(dataframes, output_dir: Path):
    """
    Create individual charts for each dataset.

    Args:
        dataframes (dict): A dictionary where keys are dataset names (e.g., 'gold', 'tesla', 'sp500')
                          and values are the corresponding DataFrames.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, df in dataframes.items():
        # Normalize column names to lowercase
        df.columns = [col.lower() for col in df.columns]

        if 'date' in df.columns and 'close' in df.columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines', name=name))

            # Update layout
            fig.update_layout(
                title=f"{name} Price Chart",
                xaxis_title="Date",
                yaxis_title="Value",
                template="plotly_dark"
            )

            if name.lower() == "gold":  # Ensure case-insensitive match
                # Generate a specific chart for Gold
                fig.update_layout(
                    title="Gold Daily Price Chart",
                    xaxis_title="Date",
                    yaxis_title="Gold Price (USD)",
                    template="plotly_white"
                )

            # -----------------------------
            # Save chart with timestamp
            # -----------------------------
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = output_dir / f"{name.lower()}_{timestamp}.html"

            fig.write_html(str(filename))
            print(f"Saved chart: {filename}")

            # Open in default browser
            webbrowser.open(filename.resolve().as_uri())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Plotly HTML charts for cleaned market datasets.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory containing cleaned CSVs and where charts will be written (default: output)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    output_dir = Path(args.output_dir)
    data_dir = output_dir

    files = {
        "Gold": data_dir / "cleaned_gold_data.csv",
        "Tesla": data_dir / "cleaned_tesla_data.csv",
        "S&P500": data_dir / "cleaned_sp500_data.csv",
    }

    dataframes = {}
    for name, file_path in files.items():
        if file_path.exists():
            df = pd.read_csv(file_path)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date column is in datetime format
            dataframes[name] = df
            print(f"Loaded data for {name}: {file_path}")
        else:
            print(f"Error: {file_path} not found. Please run the data processing step to generate it.")

    if dataframes:
        print("Dataframes passed to chart creation:", dataframes.keys())
        create_individual_charts(dataframes, output_dir)
    else:
        print("No data available to display the charts.")
