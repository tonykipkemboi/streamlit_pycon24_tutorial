# Advanced Streamlit for Python Developers: A PyCon US `24 Tutorial

_By [Caroline Frasca](https://us.pycon.org/2024/speaker/profile/89/) and [Tony Kipkemboi](https://us.pycon.org/2024/speaker/profile/90/)_

This repository hosts the code for the Advanced Streamlit for Python Developers PyCon US 2024 tutorial talk that will take place in Pittsburgh, PA.

Streamlit is a faster way to build and share data apps. Streamlit turns data scripts into shareable web apps in minutes. All in pure Python. No front-end experience required.

Check out our [docs](https://docs.streamlit.io/) to get started!

## 🚀 Getting Started

To run the GitHub Repository Analytics Dashboard locally, follow these steps:

1. Clone the repository:

   ```md
   git clone https://github.com/tonykipkemboi/streamlit_pycon24_tutorial.git
   ```

2. Navigate to the project directory:

   ```md
   cd streamlit_pycon24_tutorial
   ```

3. Set up your OpenAI API key:

   - Create a file named `.streamlit/secrets.toml` in the project directory (see example file in `.streamlit/example_secrets.toml`)
   - Add your OpenAI API key to the file in the following format:

     ```md
     OPENAI_API_KEY = "your_api_key_here"
     ```

4. Install the required dependencies:

   ```md
   pip install -r requirements.txt
   ```

5. Run the Streamlit app:

   ```md
   streamlit run 01_📈_Repository_analytics.py
   ```

6. Open your web browser and visit `http://localhost:8501` to access the dashboard.

## 📂 Repository Structure

The repository contains the following files:

- `01_📈_Repository_analytics.py`: The main Streamlit app file that contains the code for the Streamlit GitHub Repository Analytics Dashboard.
- `02_💬_Chat_with_the_Streamlit_docs.py`: A chatbot app that demonstrates how to chat with the Streamlit documentation using LlamaIndex and OpenAI.
- `data/`: Directory containing the CSV files used for data analysis.
- `docs/`: Directory containing the Streamlit documentation files for the chat app.
- `requirements.txt`: File listing the required Python dependencies.

## 📊 Features

### 1. GitHub Repository Analytics Dashboard

The GitHub Repository Analytics Dashboard provides the following features:

- ⏰ **Code Frequency**: Visualize code changes over time, including weekly code changes comparison and cumulative code changes.
- 📬 **Commit Activity**: Track the total number of commits, average weekly commits, and week-over-week change.
- 👩‍💻 **Contributors**: Analyze contributors and their activity, view contributions over time for selected users, and explore filtered data.

### 2. Chat with the Streamlit Docs

A chat app that allows you to interact with the Streamlit documentation using natural language queries. Features include:

- 💬 **Streamlit UI**: Ask questions about Streamlit's open-source Python library using natural language and get responses from the LLM.
- 🧠 **Powered by LlamaIndex**: The chat app leverages [LlamaIndex](https://www.llamaindex.ai/?gad_source=1&gclid=CjwKCAjwrvyxBhAbEiwAEg_Kgvh_e5ZuJINu47FgMRntEWXEtO6an_TCqXmVJs0P9XeKUohTtSuexhoCCaIQAvD_BwE) to efficiently search and retrieve relevant information from the Streamlit documentation.
- 🤖 **OpenAI Integration**: The app uses OpenAI's GPT-3.5-turbo model to generate human-like responses based on the retrieved information.

## 💡 Tutorial

By following this tutorial, you'll learn how to:

- Set up a Streamlit app and create tabs for different analytics views
- Implement a data loading function to handle CSV files
- Create visualizations for code frequency, commit activity, and contributor analysis
- Interact with the dashboard using sliders, dropdowns, and expandable sections
- Customize the app's appearance and layout
- Use the latest Streamlit feature `@st.experimental_fragment`; a new decorator that turns any function into a "fragment" that can run independently of the wider page

## 📧 Contact

If you have any questions or feedback, feel free to reach out to us in the [Streamlit forum](https://discuss.streamlit.io/). We'd love to hear from you! 💬

Happy Streamlit-ing! 🎈
