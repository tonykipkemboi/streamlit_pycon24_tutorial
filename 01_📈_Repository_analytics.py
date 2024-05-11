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
            f"File not found: {
                filepath}. Please check the file path.",
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

    with tab1:
        st.subheader("GitHub code change visualization")
        st.info("Visualize code changes over time.", icon="ℹ️")

        # Load and preprocess code frequency data
        code_freq_data = load_data("data/streamlit_code_frequency_stats.csv")
        code_freq_data["week"] = pd.to_datetime(
            code_freq_data["week"], unit="s"
        ).dt.date

        with st.expander("Show raw data"):
            st.dataframe(code_freq_data)

        # Implement a date range slider for selecting the period of interest
        min_week = code_freq_data["week"].min()
        max_week = code_freq_data["week"].max()
        start_week, end_week = st.slider(
            "Select Date Range",
            min_value=min_week,
            max_value=max_week,
            value=(min_week, max_week),
            format="MM/DD/YYYY",
        )

        # Filter data based on the selected date range
        filtered_data = code_freq_data[
            (code_freq_data["week"] >= start_week)
            & (code_freq_data["week"] <= end_week)
        ]

        st.subheader("Weekly code changes comparison")
        # Adjust deletions for visualization
        filtered_data["positive_deletions"] = filtered_data["deletions"].abs()

        # Display area chart for additions and deletions
        st.area_chart(
            filtered_data.set_index("week")[["additions", "deletions"]],
            color=["#00FF00", "#FF0000"],
        )

        # Display cumulative code changes over time
        st.subheader("Cumulative code changes")
        filtered_data["cumulative_additions"] = filtered_data["additions"].cumsum()
        filtered_data["cumulative_deletions"] = filtered_data["deletions"].cumsum()
        st.scatter_chart(
            filtered_data.set_index("week")[
                ["cumulative_additions", "cumulative_deletions"]
            ]
        )

    with tab2:
        st.subheader("Total commits over the past year")
        st.info("Track total number of commits.", icon="ℹ️")

        commit_activity_data = load_data("data/streamlit_commit_activity_stats.csv")
        commit_activity_data["week"] = pd.to_datetime(
            commit_activity_data["week"], unit="s"
        )

        with st.expander("Show raw data"):
            st.dataframe(commit_activity_data)

        # Display metrics for commit activity
        total_commits = commit_activity_data["total"].sum()
        average_commits = commit_activity_data["total"].mean()
        weekly_change = commit_activity_data["total"].pct_change().iloc[-1] * 100
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Commits", int(total_commits))
        col2.metric("Average Weekly Commits", f"{average_commits:.2f}")
        col3.metric("Week-over-Week Change", f"{weekly_change:.2f}%")

        st.bar_chart(commit_activity_data.set_index("week")["total"])

    with tab3:
        st.subheader("Contributor analysis")
        st.info("Analyze contributors and their activity.", icon="ℹ️")

        # Load and preprocess contributor data
        contributor_data = load_data("data/streamlit_contributor_stats.csv")
        contributor_data.rename(
            columns={"a": "additions", "d": "deletions", "c": "commits", "w": "date"},
            inplace=True,
        )
        contributor_data["date"] = pd.to_datetime(contributor_data["date"], unit="s")

        # Drop columns not needed for the analysis
        columns_to_drop = [
            "Unnamed: 0",
            "author_node_id",
            "author_avatar_url",
            "author_gravatar_id",
        ]
        contributor_data = contributor_data.drop(
            columns=columns_to_drop, errors="ignore"
        )

        with st.expander("Show raw data"):
            st.dataframe(contributor_data)

        # Calculate total activity for each contributor
        contributor_data["total_activity"] = (
            contributor_data["additions"]
            + contributor_data["deletions"]
            + contributor_data["commits"]
        )

        # Group by author to summarize total activity, sorted by activity level
        activity_by_user = (
            contributor_data.groupby("author_login")["total_activity"]
            .sum()
            .sort_values(ascending=False)
        )
        user_list = activity_by_user.index.tolist()
        selected_user = st.selectbox("Select a User", user_list)

        # Filter data for the selected user and adjust date range using a slider
        user_data = contributor_data[contributor_data["author_login"] == selected_user]
        min_date = user_data["date"].min().to_pydatetime()
        max_date = user_data["date"].max().to_pydatetime()
        start_date, end_date = st.slider(
            "Select date range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD",
        )
        filtered_data = user_data[
            (user_data["date"] >= start_date) & (user_data["date"] <= end_date)
        ]

        @st.experimental_fragment
        def plot_chart() -> None:
            """Plot data"""
            fig = px.line(
                filtered_data,
                x="date",
                y=["additions", "deletions", "commits"],
                labels={
                    "value": "Number of Contributions",
                    "variable": "Type of Contribution",
                },
                title=f"Interactive Contributions of {
                    selected_user} Over Time",
            )
            fig.update_traces(mode="lines+markers")

            st.plotly_chart(fig, use_container_width=True)

        chart, dataset = st.columns(2)

        with chart:
            st.subheader(f"Contributions over time for {selected_user}")
            plot_chart()

        with dataset:
            st.subheader(f"Show filtered data for {selected_user}")
            st.data_editor(filtered_data)


if __name__ == "__main__":
    main()
