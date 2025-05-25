import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

def plot_moving_average(df: pd.DataFrame, tickers: list):
    st.title("📊 Moving Average Analysis")
    st.subheader("Stock Price with 30-Day Rolling Mean and Standard Deviation")

    if df.empty:
        st.warning("No data available for moving average analysis.")
        return

    # Handle multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        data_close = df['Close'].copy()
    else:
        data_close = df.select_dtypes(include=['float64', 'int64']).copy()

    if data_close.empty:
        st.info("No valid columns found for moving average analysis.")
        return

    # Calculate the 30-day rolling mean and standard deviation
    for ticker in tickers:
        ticker = ticker.strip()
        if ticker in data_close.columns:
            data_close[f'{ticker}_rolling_mean'] = data_close[ticker].rolling(window=30).mean()
            data_close[f'{ticker}_rolling_std'] = data_close[ticker].rolling(window=30).std()

    # Create a 3x2 subplot grid (max 6 tickers)
    rows, cols = 3, 2
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[f"{ticker} Stock Price with Rolling Statistics" for ticker in tickers[:6]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    for i, ticker in enumerate(tickers[:6]):  # Limit to 6 for 3x2 grid
        ticker = ticker.strip()
        if ticker not in data_close.columns:
            continue
        row = i // 2 + 1
        col_idx = i % 2 + 1

        # Create a temporary DataFrame for Plotly Express
        plot_df = data_close[[ticker, f'{ticker}_rolling_mean', f'{ticker}_rolling_std']].reset_index()

        # Plot stock price
        price_fig = px.line(
            plot_df,
            x='Date',
            y=ticker,
            labels={'value': 'Price', 'Date': 'Date'},
            color_discrete_sequence=['white']
        )
        for trace in price_fig.data:
            trace.name = f"{ticker} Price"
            fig.add_trace(trace, row=row, col=col_idx)

        # Plot rolling mean
        mean_fig = px.line(
            plot_df,
            x='Date',
            y=f'{ticker}_rolling_mean',
            labels={'value': 'Price', 'Date': 'Date'},
            color_discrete_sequence=['red']
        )
        for trace in mean_fig.data:
            trace.name = 'Rolling Mean'
            fig.add_trace(trace, row=row, col=col_idx)

        # Plot rolling standard deviation
        std_fig = px.line(
            plot_df,
            x='Date',
            y=f'{ticker}_rolling_std',
            labels={'value': 'Price', 'Date': 'Date'},
            color_discrete_sequence=['green']
        )
        for trace in std_fig.data:
            trace.name = 'Rolling Std'
            fig.add_trace(trace, row=row, col=col_idx)

        fig.update_xaxes(title_text="Date", row=row, col=col_idx)
        fig.update_yaxes(title_text="Price", row=row, col=col_idx)

    fig.update_layout(
        height=800,
        width=1000,
        showlegend=True,
        title_text="Stock Price with Rolling Statistics",
        title_x=0.5
    )
    st.plotly_chart(fig, use_container_width=True)