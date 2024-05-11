import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime


@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data


def main():
    st.set_page_config(layout="wide", page_icon="📊")

    st.title('📊 GitHub repository analytics dashboard', anchor=False)

    tab1, tab2, tab3 = st.tabs(
        ["⏰ Code frequency", "📬 Commit activity", "👩‍💻 Contributors"])

    with tab1:
        st.subheader('GitHub Code Change Visualization')
        st.info(
            'Code changes in a GitHub repository over time.',
            icon="ℹ️"
        )
        # Load data from CSV file
        code_freq_data = load_data('data/streamlit_stats_code_frequency.csv')

        # Convert week column to datetime
        code_freq_data['week'] = pd.to_datetime(
            code_freq_data['week'], unit='s')
        code_freq_data['week'] = code_freq_data['week'].dt.date

        with st.expander("Show raw data"):
            st.dataframe(code_freq_data)

        # Date range slider
        min_week = code_freq_data['week'].min()
        max_week = code_freq_data['week'].max()
        start_week, end_week = st.slider("Select Date Range",
                                         min_value=min_week,
                                         max_value=max_week,
                                         value=(min_week, max_week),
                                         format='MM/DD/YYYY')

        # Filter data based on the selected date range
        filtered_data = code_freq_data[(code_freq_data['week'] >= start_week) & (
            code_freq_data['week'] <= end_week)]

        st.subheader('Weekly Code Changes Comparison')

        # Keep deletions as negative for visualization but show as positive in data view
        filtered_data['positive_deletions'] = filtered_data['deletions'].abs()

        st.area_chart(filtered_data.set_index(
            'week')[['additions', 'deletions']], color=["#00FF00", "#FF0000"])

        # Convert deletions to positive values for visualization
        filtered_data['deletions'] = filtered_data['deletions'].abs()
        filtered_data['cumulative_additions'] = filtered_data['additions'].cumsum()
        filtered_data['cumulative_deletions'] = filtered_data['deletions'].cumsum()

        st.subheader('Cumulative Code Changes')
        st.scatter_chart(filtered_data.set_index('week')[
            ['cumulative_additions', 'cumulative_deletions']])

    with tab2:
        st.subheader('Total Commits Over Time')
        commit_activity_data = load_data(
            'data/streamlit_stats_commit_activity.csv')

        commit_activity_data['week'] = pd.to_datetime(
            commit_activity_data['week'], unit='s')

        with st.expander("Show raw data"):
            st.dataframe(commit_activity_data)
        total_commits = commit_activity_data['total'].sum()
        average_commits = commit_activity_data['total'].mean()
        weekly_change = commit_activity_data['total'].pct_change(
        ).iloc[-1] * 100

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Total commits", value=int(
            total_commits))
        col2.metric(label="Average weekly commits",
                    value=f"{average_commits:.2f}")
        col3.metric(label="Week-over-week change",
                    value=f"{weekly_change:.2f}%")

        st.bar_chart(commit_activity_data.set_index('week')['total'])

    with tab3:
        st.subheader('Contributor analysis')

        # Load the data
        contributor_data = load_data(
            'data/streamlit_stats_contributors.csv')

        # Rename columns
        contributor_data.rename(columns={
            'a': 'additions',
            'd': 'deletions',
            'c': 'commits',
            'w': 'date'
        }, inplace=True)

        # Convert the 'date' column from the given datetime format
        contributor_data['date'] = pd.to_datetime(contributor_data['date'])

        # Drop unnecessary columns
        columns_to_drop = ['Unnamed: 0', 'author_node_id',
                           'author_avatar_url', 'author_gravatar_id']
        contributor_data = contributor_data.drop(
            columns=columns_to_drop, errors='ignore')

        with st.expander("Show raw data"):
            st.dataframe(contributor_data)

        # Calculate the total activity for each user
        contributor_data['total_activity'] = contributor_data['additions'] + \
            contributor_data['deletions'] + contributor_data['commits']

        # Group by author and sum their activities, then sort by total activity in descending order
        activity_by_user = contributor_data.groupby(
            'author_login')['total_activity'].sum().sort_values(ascending=False)
        user_list = activity_by_user.index.tolist()
        selected_user = st.selectbox('Select a User', user_list)

        # Filter the data for the selected user
        user_data = contributor_data[contributor_data['author_login']
                                     == selected_user]

        # Convert pandas.Timestamp to native Python datetime for slider compatibility
        min_date = user_data['date'].min().to_pydatetime()
        max_date = user_data['date'].max().to_pydatetime()

        # Now use these in the slider
        start_date, end_date = st.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(
            min_date, max_date), format='YYYY-MM-DD')

        # Filter data based on selected range
        filtered_data = user_data[(user_data['date'] >= start_date) & (
            user_data['date'] <= end_date)]

        @st.experimental_fragment
        def plot_chart(user_data, start_date, end_date):
            """Plot data"""
            fig = px.line(filtered_data, x='date', y=['additions', 'deletions', 'commits'],
                          labels={'value': 'Number of Contributions',
                                  'variable': 'Type of Contribution'},
                          title=f'Interactive Contributions of {selected_user} Over Time')
            fig.update_traces(mode='lines+markers')

            st.plotly_chart(fig, use_container_width=True)

        chart, dataset = st.columns(2)

        with chart:
            st.subheader(f"Contributions over time for {selected_user}")
            plot_chart(user_data, start_date, end_date)

        with dataset:
            st.subheader(f"Show filtered data for {selected_user}")
            st.data_editor(filtered_data)


if __name__ == "__main__":
    main()
