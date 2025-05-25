import streamlit as st
import pandas as pd

def filter_columns(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    try:
        # Only keep specified columns that exist in the DataFrame
        df = df[[col for col in cols if col in df.columns]]
        st.success("Columns Filtered Successfully")
        return df
    except Exception as e:
        st.error(f"Error filtering columns: {e}")
        return df
    

def create_line_chart(df: pd.DataFrame):
    st.subheader("Line Chart")
    st.line_chart(df['Close'], use_container_width=True)

def describe_data(df: pd.DataFrame):
    st.subheader("Data Description")
    st.write("Data Shape:", df.shape)
    st.write("Data Types:", df.dtypes)
    st.write("Missing Values:", df.isnull().sum())
    st.write("Statistical Summary:")
    st.dataframe(df.describe())