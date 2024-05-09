import streamlit as st
import requests
import pandas as pd
import time


@st.cache_data
def get_api_data(url, headers, retries=3):
    for _ in range(retries):
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 202:
            time.sleep(10)  # Wait for 10 seconds before retrying
        elif response.status_code == 403:
            # Handle lack of permissions
            st.error("Permission Denied: probably not your repo.", icon="🚫")
            return "Permission Denied"
        else:
            st.error(f"Failed to fetch data: {
                     response.status_code}", icon="⛔️")
            return None
    st.error("Request failed or data not ready after retries.")
    return None


def display_traffic_data(data, title):
    if data:
        df = pd.DataFrame(data)
        # Convert Unix timestamps to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Optionally, format the datetime as a string in a more readable form
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d')
        st.subheader(title)
        with st.expander("Views dataframe"):
            st.dataframe(df)
        st.line_chart(df.set_index('timestamp')[['count', 'uniques']])


def display_commit_activity(owner, repo, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity"
    data = get_api_data(url, headers)
    if data:
        df = pd.DataFrame(data)
        df['week'] = pd.to_datetime(df['week'], unit='s')
        st.line_chart(df.set_index('week')['total'])


def display_contributor_commits(owner, repo, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/contributors"
    data = get_api_data(url, headers)
    if data:
        contributors = {item['author']['login']: sum(
            [week['c'] for week in item['weeks']]) for item in data}
        df = pd.DataFrame(list(contributors.items()),
                          columns=['Contributor', 'Commits'])
        st.bar_chart(df.set_index('Contributor'))
    else:
        st.write("No contributor commits in this repo.")


def display_code_frequency(owner, repo, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/code_frequency"
    data = get_api_data(url, headers)
    if data:
        df = pd.DataFrame(data, columns=['week', 'additions', 'deletions'])
        df['week'] = pd.to_datetime(df['week'], unit='s')
        df.set_index('week', inplace=True)
        # Create two separate columns for additions and deletions
        # Convert additions to positive values (API returns them as negatives)
        df['additions'] = df['additions'].abs()
        df['deletions'] = df['deletions'].abs()
        st.line_chart(df[['additions', 'deletions']])


def app():
    st.set_page_config(page_title="GitHub Repo Metrics",
                       layout="wide", page_icon="📈")
    st.title("GitHub Repository Metrics Dashboard 📈")

    # Sidebar for inputs
    with st.sidebar:
        token = st.text_input("GitHub Token", type="password")
        owner = st.text_input("Repository Owner", value="octocat")
        repo = st.text_input("Repository Name", value="Hello-World")
        submitted = st.button("Fetch data")

    headers = {"Authorization": f"token {token}"}

    # Tabs for different metrics
    tab1, tab2, tab3 = st.tabs(
        ["📈 Repo Traffic", "📊 Repo Stats", "📉 Engagement Metrics"])

    if submitted:
        # Check if the token is valid and has access to the repo
        repo_url = f"https://api.github.com/repos/{owner}/{repo}"
        repo_data = get_api_data(repo_url, headers)
        if not repo_data:
            st.error(
                "Please ensure the repository exists and your token has the correct permissions.")
            return

        # Repository Traffic
        with tab1:
            st.subheader("Repository Traffic ")
            views_url = f"https://api.github.com/repos/{
                owner}/{repo}/traffic/views"
            clones_url = f"https://api.github.com/repos/{
                owner}/{repo}/traffic/clones"
            views_data = get_api_data(views_url, headers)
            clones_data = get_api_data(clones_url, headers)

            # Display views data
            if views_data and 'views' in views_data:
                display_traffic_data(views_data['views'], "Views over Time")

            # Display clones data
            if clones_data and 'clones' in clones_data:
                display_traffic_data(clones_data['clones'], "Clones over Time")

        # Repository Statistics
        with tab2:
            st.subheader("Repository Statistics")

            st.subheader("Commit activity")
            display_commit_activity(owner, repo, headers)

            st.subheader("Code frequency")
            display_code_frequency(owner, repo, headers)

            st.subheader("Contributor commits")
            display_contributor_commits(owner, repo, headers)

        # Engagement Metrics
        with tab3:
            st.subheader("Engagement Metrics")
            repo_details_url = f"https://api.github.com/repos/{owner}/{repo}"
            repo_details_data = get_api_data(repo_details_url, headers)
            if repo_details_data:
                col1, col2, col3 = st.columns(3)
                col1.metric("Forks", repo_details_data['forks_count'])
                col2.metric("Stars", repo_details_data['stargazers_count'])
                col3.metric("Watchers", repo_details_data['watchers_count'])


if __name__ == "__main__":
    app()
