import streamlit as st
import pandas as pd
import plotly.express as px

def plot_bollinger_bands(df: pd.DataFrame, tickers: list):
    st.title("📊 Bollinger Bands Analysis")
    st.subheader("Stock Price with Bollinger Bands and Volatility")

    if df.empty:
        st.warning("No data available for Bollinger Bands analysis.")
        return

    # Handle multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        data_close = df['Close'].copy()
    else:
        data_close = df.select_dtypes(include=['float64', 'int64']).copy()

    if data_close.empty:
        st.info("No valid columns found for Bollinger Bands analysis.")
        return

    # Compute Bollinger Bands and volatility
    for ticker in tickers:
        ticker = ticker.strip()
        if ticker in data_close.columns:
            data_close[f'{ticker}_rolling_mean'] = data_close[ticker].rolling(window=30).mean()
            data_close[f'{ticker}_rolling_std'] = data_close[ticker].rolling(window=30).std()
            data_close[f'{ticker}_upper_band'] = data_close[f'{ticker}_rolling_mean'] + (data_close[f'{ticker}_rolling_std'] * 2)
            data_close[f'{ticker}_lower_band'] = data_close[f'{ticker}_rolling_mean'] - (data_close[f'{ticker}_rolling_std'] * 2)
            data_close[f'{ticker}_daily_return'] = data_close[ticker].pct_change()
            data_close[f'{ticker}_volatility'] = data_close[f'{ticker}_daily_return'].rolling(window=30).std()

    # Display the DataFrame and missing values
    st.write("Bollinger Bands Data:")
    st.dataframe(data_close)
    st.write("Missing Values:")
    st.write(data_close.isna().sum())

    # Plot Bollinger Bands for each ticker in a single column
    for ticker in tickers[:6]:  # Limit to 6 tickers to avoid overwhelming the display
        ticker = ticker.strip()
        if ticker not in data_close.columns:
            continue

        # Create a temporary DataFrame for Plotly Express
        plot_df = data_close[[ticker, f'{ticker}_rolling_mean', f'{ticker}_upper_band', f'{ticker}_lower_band']].reset_index()

        # Rename columns for clarity
        plot_df.columns = ['Date', 'Price', 'Rolling Mean', 'Upper Band', 'Lower Band']

        # Create a single figure for the ticker
        fig = px.line(
            plot_df,
            x='Date',
            y=['Price', 'Rolling Mean', 'Upper Band', 'Lower Band'],
            labels={'value': 'Price', 'Date': 'Date', 'variable': 'Metric'},
            color_discrete_map={
                'Price': 'blue',
                'Rolling Mean': 'orange',
                'Upper Band': 'green',
                'Lower Band': 'red'
            }
        )

        # Update line styles for upper and lower bands
        for trace in fig.data:
            if trace.name == 'Upper Band' or trace.name == 'Lower Band':
                trace.line = dict(dash='dash')

        # Update layout
        fig.update_layout(
            height=400,
            width=1000,
            showlegend=True,
            title_text=f"Bollinger Bands for {ticker}",
            title_x=0.5,
            xaxis_title="Date",
            yaxis_title="Price"
        )

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)