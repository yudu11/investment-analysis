# chart_visualizer.py

import plotly.graph_objects as go
import pandas as pd
import os

def create_interactive_chart(dataframes):
    """
    Create an interactive chart to display the data.

    Args:
        dataframes (dict): A dictionary where keys are dataset names (e.g., 'gold', 'tesla', 'sp500')
                          and values are the corresponding DataFrames.
    """
    fig = go.Figure()

    # Add traces for each dataset
    for name, df in dataframes.items():
        if 'Date' in df.columns and 'Close' in df.columns:
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name=name))

    # Update layout
    fig.update_layout(
        title="Interactive Chart of Gold, Tesla, and S&P500",
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_dark"
    )

    # Show the chart
    fig.show()

if __name__ == "__main__":
    # Example usage
    files = {
        "Gold": "cleaned_gold_data.csv",
        "Tesla": "cleaned_tesla_data.csv",
        "S&P500": "cleaned_sp500_data.csv"
    }

    dataframes = {}
    for name, file in files.items():
        if os.path.exists(file):
            dataframes[name] = pd.read_csv(file)
        else:
            print(f"Error: {file} not found. Please run the data processing step to generate it.")

    if dataframes:
        create_interactive_chart(dataframes)
    else:
        print("No data available to display the chart.")
