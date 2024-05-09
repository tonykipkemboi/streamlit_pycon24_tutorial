import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Howdy! :wave:", anchor=False)

st.subheader("This app lets you chat with your repo and get analytics!")

instructions = """
---

**Instructions:**

- Create a repo on Github.
- Add the repo link to the sidebar.
- Select the repo from the sidebar.
- Start chatting with the bot.
- Get analytics.

---
"""

st.write(instructions)
