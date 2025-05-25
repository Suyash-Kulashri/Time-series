import streamlit as st
import yfinance as yf
import pandas as pd
from download_data import download_data
from filter_cols import filter_columns, create_line_chart, describe_data
from distribution import check_distribution, distribution_for_daily_returns
from moving_avg import plot_moving_average
from bollinger import plot_bollinger_bands
import os

# Set page configuration
st.set_page_config(
    page_title="Time Series Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for dataframes
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = pd.DataFrame()
if 'ticker_list' not in st.session_state:
    st.session_state.ticker_list = []

def title():
    st.title("📈 Time Series Analysis")
    st.subheader("Please enter your Ticker Name(s)")
    st.write("Maximum 6 tickers allowed at a time.")

    # Allow multiple tickers as comma-separated input
    ticker = st.text_input("Ticker(s)", value="AAPL,NVDA", placeholder="e.g. AAPL, MSFT, GOOGL")


    if ticker:
        ticker_list = [t.strip() for t in ticker.split(",") if t.strip()]
        st.session_state.ticker_list = ticker_list
    else:
        st.session_state.ticker_list = []

    with st.sidebar:
        start_date = st.date_input("Start Date", value=pd.to_datetime('2019-01-01'))
        end_date = st.date_input("End Date", value=pd.to_datetime('2024-12-31'))

    return ticker, start_date, end_date

def main():
    ticker, start_date, end_date = title()

    # Download data section
    if st.button("Download Data"):
        if ticker and start_date and end_date:
            if end_date <= start_date:
                st.error("End date must be after start date")
                return
            
            # Split tickers and remove whitespace
            ticker_list = [t.strip() for t in ticker.split(",") if t.strip()]
            if not ticker_list:
                st.warning("Please provide at least one valid ticker symbol")
                return

            # Download data for all tickers
            try:
                st.session_state.df = download_data(ticker_list, start_date, end_date)
                st.session_state.filtered_df = st.session_state.df.copy()  # Initialize filtered_df
                if not st.session_state.df.empty:
                    st.write("Downloaded Data:")
                    st.dataframe(st.session_state.df)
                    # Save the downloaded data as a CSV in the root folder
                    csv_filename = "data.csv"
                    st.session_state.df.to_csv(csv_filename, index=True)
                
            except Exception as e:
                st.error(f"Error downloading data: {str(e)}")
        else:
            st.warning("Please provide ticker symbol(s) and date range")

    # Always display downloaded data if available
    if not st.session_state.df.empty:
        st.write("Current Data:")
        st.dataframe(st.session_state.df)

    # Column filtering section
    if not st.session_state.df.empty:
        cols = st.multiselect(
            "Select columns to keep",
            st.session_state.df.columns.tolist(),
            default=st.session_state.df.columns.tolist()
        )
        
        if st.button("Filter Columns"):
            try:
                st.session_state.filtered_df = filter_columns(st.session_state.df, cols)
                if not st.session_state.filtered_df.empty:
                    st.write("Filtered Data:")
                    st.dataframe(st.session_state.filtered_df)
                    # Save filtered data as CSV
                    filtered_csv_filename = "filtered_data.csv"
                    st.session_state.filtered_df.to_csv(filtered_csv_filename, index=True)
                else:
                    st.warning("Filtered data is empty. Please select valid columns.")
            except Exception as e:
                st.error(f"Error filtering columns: {str(e)}")
        
        # Always display filtered data if available
        if not st.session_state.filtered_df.empty:
            st.write("Current Filtered Data:")
            st.dataframe(st.session_state.filtered_df)
            # Data description section
            describe_data(st.session_state.filtered_df)
            # Line chart section
            create_line_chart(st.session_state.filtered_df)

        # Distribution analysis section
        if st.button("Check Distribution"):
            try:
                check_distribution(st.session_state.filtered_df)
                ticker_list = [t.strip() for t in ticker.split(",") if t.strip()]
                distribution_for_daily_returns(st.session_state.filtered_df, tickers=ticker_list)
            except Exception as e:
                st.error(f"Error in distribution analysis: {str(e)}")


        # Moving average analysis section
        if st.button("Moving Average Analysis"):
            try:
                if not st.session_state.filtered_df.empty:
                    ticker_list = [t.strip() for t in ticker.split(",") if t.strip()]
                    plot_moving_average(st.session_state.filtered_df, tickers=ticker_list)
                else:
                    st.warning("Filtered data is empty. Please filter columns first.")
            except Exception as e:
                st.error(f"Error in moving average analysis: {str(e)}")
        

        # Bollinger Bands analysis section
        if st.button("Show Bollinger Bands"):
            try:
                ticker_list = [t.strip() for t in ticker.split(",") if t.strip()]
                plot_bollinger_bands(st.session_state.filtered_df, tickers=ticker_list)
            except Exception as e:
                st.error(f"Error in Bollinger Bands analysis: {str(e)}")
        
    else:
        st.info("No data available. Please download data first.")

# Ensure the root folder exists for saving CSV files


if __name__ == "__main__":
    main()