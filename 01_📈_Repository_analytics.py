import streamlit as st
import pandas as pd
import ast


@st.cache_data
def load_data(filepath):
    data = pd.read_csv(filepath)
    return data


def main():
    st.set_page_config(layout="centered", page_icon="📊")

    st.title('GitHub Repository Analytics Dashboard 📊', anchor=False)

    tab1, tab2, tab3 = st.tabs(
        ["⏰ Code frequency", "📬 Commit activity", "👩‍💻 Contributors"])

    with tab1:
        st.subheader('GitHub Code Change Visualization')
        st.info(
            'Code changes in a GitHub repository over time.',
            icon="ℹ️"
        )
        code_freq_data = load_data('data/streamlit_stats_code_frequency.csv')
        code_freq_data['week'] = pd.to_datetime(
            code_freq_data['week'], unit='s')
        with st.expander("Show raw data"):
            st.dataframe(code_freq_data)
        st.subheader('Weekly Code Changes Comparison')
        st.area_chart(code_freq_data.set_index(
            'week')[['additions', 'deletions']], color=["#00FF00", "#FF0000"])

        # Convert deletions to positive values for visualization
        code_freq_data['deletions'] = code_freq_data['deletions'].abs()
        code_freq_data['cumulative_additions'] = code_freq_data['additions'].cumsum()
        code_freq_data['cumulative_deletions'] = code_freq_data['deletions'].cumsum()
        st.subheader('Cumulative Code Changes')
        st.line_chart(code_freq_data.set_index('week')[
                      ['cumulative_additions', 'cumulative_deletions']])

    with tab2:
        st.subheader('Total Commits Over Time')
        commit_activity_data = load_data(
            'data/streamlit_stats_commit_activity.csv')
        with st.expander("Show raw data"):
            st.dataframe(commit_activity_data)
        total_commits = commit_activity_data['total'].sum()
        average_commits = commit_activity_data['total'].mean()
        weekly_change = commit_activity_data['total'].pct_change(
        ).iloc[-1] * 100  # last element percentage change

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Total Commits", value=int(
            total_commits))
        col2.metric(label="Average Weekly Commits",
                    value=f"{average_commits:.2f}")
        col3.metric(label="Week-onWeek Change",
                    value=f"{weekly_change:.2f}%")

        commit_activity_data['week'] = pd.to_datetime(
            commit_activity_data['week'], unit='s')
        st.bar_chart(commit_activity_data.set_index('week')['total'])

    with tab3:
        st.subheader('GitHub Contributors')
        contributors_data = load_data(
            'data/streamlit_stats_contributors.csv')

        # Convert the 'author' column's string values into actual dictionaries
        contributors_data['author'] = contributors_data['author'].apply(
            ast.literal_eval)

        # Create new columns for each key in the 'author' dictionary
        for key in contributors_data['author'].apply(lambda x: x.keys()).iloc[0]:
            contributors_data[f'author_{key}'] = contributors_data['author'].apply(
                lambda x: x.get(key))
        contributors_data.drop('author', axis=1, inplace=True)
        contributors_data['w'] = pd.to_datetime(
            contributors_data['w'], unit='s')
        with st.expander("Show raw data"):
            st.dataframe(contributors_data)

        st.subheader('Contributions by User')
        contributions_by_user = contributors_data['author_login'].value_counts(
        )
        st.bar_chart(contributions_by_user)


if __name__ == "__main__":
    main()
