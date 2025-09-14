# chart_visualizer.py

import plotly.graph_objects as go
import pandas as pd
import os

def create_individual_charts(dataframes):
    """
    Create individual charts for each dataset.

    Args:
        dataframes (dict): A dictionary where keys are dataset names (e.g., 'gold', 'tesla', 'sp500')
                          and values are the corresponding DataFrames.
    """
    for name, df in dataframes.items():
        # Normalize column names to lowercase
        df.columns = map(str.lower, df.columns)

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
            df = pd.read_csv(file)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])  # Ensure Date column is in datetime format
            dataframes[name] = df
            print(f"Loaded data for {name}: {df.head()}")  # Debug statement to check data loading
        else:
            print(f"Error: {file} not found. Please run the data processing step to generate it.")

    if dataframes:
        print("Dataframes passed to chart creation:", dataframes.keys())  # Debug statement to check datasets
        create_individual_charts(dataframes)
    else:
        print("No data available to display the charts.")
