import yfinance as yf
import pandas as pd
import streamlit as st

def download_data(ticker: str, start_date, end_date) -> pd.DataFrame:
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        st.success("Data Downloaded Successfully")
        return df
    except Exception as e:
        st.error(f"Error downloading data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error