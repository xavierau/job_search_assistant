import streamlit as st

from helpers import init_session_vars, call
from layouts.init_sidebar import init_sidebar
from layouts.init_user_profile_management import init_user_profile_management

from llm.prompts import update_system_prompt_when_profile_changed
from tools.ask_database import ask_database, ask_database_schema
from tools.cover_letter_writer import cover_letter_writer, cover_letter_writer_schema
from tools.feature_job import feature_job, feature_job_schema

init_session_vars()

tools = [
    {
        "name": "ask_database",
        "schema": ask_database_schema,
        "func": ask_database
    },
    {
        "name": "feature_job",
        "schema": feature_job_schema,
        "func": feature_job
    },
    {
        "name": "cover_letter_writer",
        "schema": cover_letter_writer_schema,
        "func": cover_letter_writer
    }
]

# setup layout
st.title("Job Search Assistant")
st.write(
    "You can ask the assistant to find jobs in UK for you and then you ask the assistant to create a cover letter for the job!")

user_profile_management = st.expander("User Profile")
init_user_profile_management(user_profile_management, update_system_prompt_when_profile_changed)

sidebar = st.sidebar
init_sidebar(sidebar)

# setup states
user_profile = st.session_state.user_profile
messages = st.session_state.messages

for message in messages:
    if (message["role"] == "assistant" or message["role"] == "user") and message["content"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        full_response = call(messages, tools, message_placeholder)

        message_placeholder.markdown(full_response)

    messages.append({"role": "assistant", "content": full_response})
