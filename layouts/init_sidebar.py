from config import Config, AppState


def update_openai_config(sidebar):
    openai_api_model = sidebar.radio(
        label="LLM Model",
        options=["gpt-3.5-turbo-1106", "gpt-4-1106-preview"],
        index=0)

    openai_api_key = sidebar.text_input("OpenAI API Key")

    return openai_api_model, openai_api_key


def show_saved_jobs(sidebar):
    featured_jobs = AppState.get_instance().get_state("featured_jobs", [])

    for featured_job in featured_jobs or []:
        print("featured job: ", featured_job)
        url = featured_job.get("url", "#")
        name = featured_job.get("name", "Job")
        sidebar.markdown(f"[{name}]({url})")


def init_sidebar(sidebar):
    sidebar.title("Config")

    # Config openai
    openai_api_model, openai_api_key = update_openai_config(sidebar)

    if sidebar.button("Update Config"):
        Config.get_instance().set_config("openai_api_key", openai_api_key)
        Config.get_instance().set_config("openai_model", openai_api_model)

    user_profile = Config.get_instance().get_config("user_profile", {})
    current_user = f"{user_profile.get('first_name')} {user_profile.get('last_name')}" if user_profile.items() else "default user"
    sidebar.write(f"<small>Current user: {current_user}<small>", unsafe_allow_html=True)
    sidebar.title("Saved Jobs")

    show_saved_jobs(sidebar)
