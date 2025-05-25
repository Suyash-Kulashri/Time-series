import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def check_distribution(df: pd.DataFrame):
    st.title("📊 Distribution Analysis")
    st.subheader("Check the distribution of your data")

    if df.empty:
        st.warning("No data available for distribution analysis.")
        return

    # Handle multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        # Extract 'Close' prices for each ticker
        numeric_cols = [col for col in df.columns if col[0] == 'Close']
        if not numeric_cols:
            st.info("No 'Close' price columns available for distribution analysis.")
            return
        # Create a DataFrame with single-level columns for plotting
        plot_df = df['Close'].copy()
    else:
        # If single-level columns, select numeric columns
        plot_df = df.select_dtypes(include=['float64', 'int64']).copy()
        numeric_cols = plot_df.columns

    if not numeric_cols:
        st.info("No numeric columns available for distribution analysis.")
        return

    # Create a 3x2 subplot grid (max 6 tickers)
    rows, cols = 3, 2
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[f"{col[1] if isinstance(col, tuple) else col} Distribution" for col in numeric_cols[:6]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    for i, col in enumerate(numeric_cols[:6]):  # Limit to 6 for 3x2 grid
        row = i // 2 + 1
        col_idx = i % 2 + 1
        col_name = col[1] if isinstance(col, tuple) else col
        hist = px.histogram(plot_df, x=col_name, nbins=50, histnorm='probability density')
        for trace in hist.data:
            fig.add_trace(trace, row=row, col=col_idx)
        fig.update_xaxes(title_text="Stock Price", row=row, col=col_idx)
        fig.update_yaxes(title_text="Frequency", row=row, col=col_idx)

    fig.update_layout(height=800, width=1000, showlegend=False, 
                     title_text="Stock Price Distributions", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def distribution_for_daily_returns(df: pd.DataFrame, tickers: list):
    st.title("📊 Daily Returns Distribution Analysis")
    st.subheader("Check the distribution of daily returns")

    if df.empty:
        st.warning("No data available for daily returns analysis.")
        return

    # Handle multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        data_close = df['Close'].copy()
    else:
        data_close = df.select_dtypes(include=['float64', 'int64']).copy()

    if data_close.empty:
        st.info("No valid columns found for daily returns analysis.")
        return

    # Calculate daily returns
    returns_cols = []
    for ticker in tickers:
        ticker = ticker.strip()
        if ticker in data_close.columns:
            data_close[f'{ticker}_daily_return'] = data_close[ticker].pct_change()
            returns_cols.append(f'{ticker}_daily_return')

    if not returns_cols:
        st.info("No valid ticker columns found for daily returns analysis.")
        return

    # Create a 3x2 subplot grid for daily returns
    rows, cols = 3, 2
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[f"{col.split('_')[0]} Daily Return Distribution" for col in returns_cols[:6]],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    for i, col in enumerate(returns_cols[:6]):  # Limit to 6 for 3x2 grid
        row = i // 2 + 1
        col_idx = i % 2 + 1
        hist = px.histogram(data_close, x=col, nbins=50, histnorm='probability density')
        for trace in hist.data:
            fig.add_trace(trace, row=row, col=col_idx)
        fig.update_xaxes(title_text="Daily Return", row=row, col=col_idx)
        fig.update_yaxes(title_text="Frequency", row=row, col=col_idx)

    fig.update_layout(height=800, width=1000, showlegend=False,
                     title_text="Daily Returns Distributions", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)