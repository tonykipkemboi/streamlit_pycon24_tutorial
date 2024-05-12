import streamlit as st
import pandas as pd
import plotly.express as px
from pandas import DataFrame


@st.cache_data
def load_data(filepath: str) -> DataFrame:
    """
    Load data from a CSV file located at the specified filepath.

    Args:
        filepath (str): The path to the CSV file to be loaded.

    Returns:
        DataFrame: A DataFrame containing the loaded data, or an empty DataFrame if an error occurs.

    Raises:
        FileNotFoundError: If the CSV file cannot be found at the specified path.
        pd.errors.EmptyDataError: If the CSV file is empty.
        Exception: For any other exceptions that may occur during file loading.
    """
    try:
        data = pd.read_csv(filepath)
        if data.empty:
            st.error("No data found in the CSV file.", icon="🚨")
        return data
    except FileNotFoundError:
        st.error(
            f"File not found: {filepath}. Please check the file path.",
            icon="🚨",
        )
    except pd.errors.EmptyDataError:
        st.error("No data found in the CSV file.", icon="🚨")
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}", icon="🚨")
    return pd.DataFrame()  # Return an empty DataFrame if any error occurs


def main():
    st.set_page_config(layout="wide", page_icon="📊")
    st.title("📊 GitHub Repository Analytics Dashboard", anchor=False)

    # Create tabs for different analytics views
    tab1, tab2, tab3 = st.tabs(
        ["⏰ Code Frequency", "📬 Commit Activity", "👩‍💻 Contributors"]
    )