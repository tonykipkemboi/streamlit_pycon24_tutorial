import subprocess
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs

import streamlit as st
from llama_index.core import PromptTemplate, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.readers.github import GithubRepositoryReader, GithubClient
from llama_index.llms.groq import Groq

st.set_page_config(
    page_title="Chat with your repo",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_github_client(github_token: str) -> GithubClient:
    """Initialize a GithubClient instance."""
    return GithubClient(github_token)


def get_groq_llm(api_key: str) -> Groq:
    """Initialize a Groq LLM instance."""
    return Groq(model="mixtral-8x7b-32768", api_key=api_key)


def parse_github_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse a GitHub repository URL to extract the owner and repository name."""
    parsed_url = urlparse(url)
    if "github.com" in parsed_url.netloc:
        parts = parsed_url.path.strip("/").split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]
    return None, None


def get_latest_commit_sha(repo_owner: str, repo_name: str) -> Optional[str]:
    """Get the latest commit SHA from a GitHub repository."""
    repo_url = f"https://github.com/{repo_owner}/{repo_name}.git"
    try:
        output = subprocess.check_output(
            ["git", "ls-remote", repo_url, "HEAD"])
        commit_sha = output.decode().split("\t")[0]
        return commit_sha
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.output.decode()}")
        return None


def load_github_repo(github_client: GithubClient, repo_owner: str, repo_name: str, commit_sha: str):
    """Load a GitHub repository."""
    reader = GithubRepositoryReader(
        github_client=github_client,
        owner=repo_owner,
        repo=repo_name,
        filter_file_extensions=(
            [".md", ".py", ".ipynb", ".js", ".ts"],
            GithubRepositoryReader.FilterType.INCLUDE,
        ),
        verbose=True,
        concurrent_requests=5,
    )
    return reader.load_data(commit_sha=commit_sha)


def load_embedding_model(model_name: str = "Snowflake/snowflake-arctic-embed-m") -> HuggingFaceEmbedding:
    """Load snowflake-arctic-embedding model."""
    return HuggingFaceEmbedding(model_name=model_name, trust_remote_code=True)


def index_data(data, embed_model: HuggingFaceEmbedding) -> VectorStoreIndex:
    """Index data."""
    Settings.embed_model = embed_model
    return VectorStoreIndex.from_documents(data)


def main():
    """Main function."""
    st.title("Chat with your repo 💬", anchor=False)

    github_token = st.secrets["GITHUB_TOKEN"]
    groq_api_key = st.secrets["GROQ_API_KEY"]

    if not github_token or not groq_api_key:
        st.error("GitHub token and Groq API key are required.")
        return

    if github_url := st.text_input("Enter GitHub repository URL"):
        repo_owner, repo_name = parse_github_url(github_url)
        if repo_owner and repo_name:
            commit_sha = get_latest_commit_sha(repo_owner, repo_name)
            if commit_sha:
                # Code to load the repository and perform actions
                st.write("Loading GitHub Repository...")
                data = load_github_repo(
                    get_github_client(github_token), repo_owner, repo_name, commit_sha)

                st.write("Loading Embedding Model...")
                embed_model = load_embedding_model()

                st.write("Indexing Data...")
                index = index_data(data, embed_model)

                st.write("Initializing Groq LLM...")
                llm = get_groq_llm(groq_api_key)
                Settings.llm = llm  # specify llm to be used

                st.write("Querying Data...")
                query_engine = index.as_query_engine(
                    streaming=True, similarity_top_k=4)

                qa_prompt_tmpl_str = """
                You are a helpful assistant.
                You are given the following code snippet:
                ```
                {context_str}
                ```
                You need to answer the following question:
                {query_str}
                I want you to think step by step to answer the query.   
                If you don't know the answer, say "I don't know."
                Answer in markdown format.
                """
                qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
                query_engine.update_prompts(
                    {"response_synthesizer:text_qa_template": qa_prompt_tmpl})

                query = st.text_input("Query")
                if query:
                    response = query_engine.query(query)
                    st.markdown(response)
            else:
                st.error("Error: Failed to get latest commit SHA.")


if __name__ == "__main__":
    main()
