import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

def check_stationarity(df: pd.DataFrame, tickers: list):
    st.title("📊 Stationarity Analysis")
    st.subheader("Seasonal Decomposition of Stock Prices")

    if df.empty:
        st.warning("No data available for stationarity analysis.")
        return

    # Display the filtered DataFrame
    st.write("Filtered Data:")
    st.dataframe(df)

    # Handle multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        data_close = df['Close'].copy()
    else:
        data_close = df.select_dtypes(include=['float64', 'int64']).copy()

    if data_close.empty:
        st.info("No valid columns found for stationarity analysis.")
        return

    # Perform seasonal decomposition and plot for each ticker
    for ticker in tickers[:6]:  # Limit to 6 tickers to avoid overwhelming the display
        ticker = ticker.strip()
        if ticker not in data_close.columns:
            st.warning(f"Ticker {ticker} not found in data.")
            continue

        # Perform seasonal decomposition
        try:
            result = seasonal_decompose(data_close[ticker], model='additive', period=365)
        except Exception as e:
            st.error(f"Error performing seasonal decomposition for {ticker}: {str(e)}")
            continue

        # Create a temporary DataFrame for Plotly Express
        plot_df = pd.DataFrame({
            'Date': data_close.index,
            'Original': data_close[ticker],
            'Trend': result.trend,
            'Seasonal': result.seasonal,
            'Residual': result.resid
        }).reset_index(drop=True)

        # Create a subplot with 4 rows (Original, Trend, Seasonal, Residual)
        fig = make_subplots(
            rows=4,
            cols=1,
            subplot_titles=[
                f"{ticker} Stock Price",
                f"{ticker} Trend Component",
                f"{ticker} Seasonal Component",
                f"{ticker} Residual Component"
            ],
            vertical_spacing=0.15  # Increased to prevent overlapping headings
        )

        # Plot Original Series
        original_fig = px.line(
            plot_df,
            x='Date',
            y='Original',
            labels={'value': 'Price', 'Date': 'Date'},
            color_discrete_sequence=['blue']
        )
        for trace in original_fig.data:
            trace.name = 'Original'
            fig.add_trace(trace, row=1, col=1)

        # Plot Trend Component
        trend_fig = px.line(
            plot_df,
            x='Date',
            y='Trend',
            labels={'value': 'Price', 'Date': 'Date'},
            color_discrete_sequence=['green']
        )
        for trace in trend_fig.data:
            trace.name = 'Trend'
            fig.add_trace(trace, row=2, col=1)

        # Plot Seasonal Component
        seasonal_fig = px.line(
            plot_df,
            x='Date',
            y='Seasonal',
            labels={'value': 'Price', 'Date': 'Date'},
            color_discrete_sequence=['orange']
        )
        for trace in seasonal_fig.data:
            trace.name = 'Seasonality'
            fig.add_trace(trace, row=3, col=1)

        # Plot Residual Component
        residual_fig = px.line(
            plot_df,
            x='Date',
            y='Residual',
            labels={'value': 'Price', 'Date': 'Date'},
            color_discrete_sequence=['red']
        )
        for trace in residual_fig.data:
            trace.name = 'Residuals'
            fig.add_trace(trace, row=4, col=1)

        # Update axes
        fig.update_xaxes(title_text="Date", row=1, col=1)
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_xaxes(title_text="Date", row=3, col=1)
        fig.update_xaxes(title_text="Date", row=4, col=1)
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="Price", row=2, col=1)
        fig.update_yaxes(title_text="Price", row=3, col=1)
        fig.update_yaxes(title_text="Price", row=4, col=1)

        # Update layout
        fig.update_layout(
            height=800,
            width=1000,
            showlegend=True,
            title_text=f"Seasonal Decomposition of {ticker} Stock Prices",
            title_x=0.5
        )

        # Display the plot
        st.plotly_chart(fig, use_container_width=True)