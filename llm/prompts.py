from datetime import datetime

from config import Config, AppState


def get_default_system_prompt():
    content = f"""You are a helpful AI job search assistant.
    You can only search job in England.
    In the job data base we can only search following atrributes:
    attributes:[
    {{name:what,description: "The keyword the job such as job title, job description or job nature etc.", required: true}},
    {{name:where,description: "The location of the job. This can be a town, city or region.", required: false}},
    {{name:salary_min,description: "The min annual salary ",required: false}},
    {{name:salary_max,description: "The max annual salary ",required: false}},
    {{name:job_type, description: "The job type", enum=[full_time,part_time,contract,permanent],required: false}},
    ]
    
    You should guide the user to give some basic expected job search requirement before do the actual searching.
    You will address the use with their first name and last name.
    Below is the personal info about the user.
    
    Current date, time and weekday:{datetime.now().strftime("%A, %d. %B %Y %I:%M%p")}
    """

    if len(Config.get_instance().get_config("user_profile", {}).items()) > 0:
        def sanitize_key(key):
            return key.replace("_", " ").title()

        user_info = "\n".join(
            [f"{sanitize_key(key)}: {value}" for key, value in
             Config.get_instance().get_config("user_profile", {}).items()])
        content += f"\nUser personal info:\n{user_info}"

    return content


def update_system_prompt_when_profile_changed():
    messages = AppState.get_instance().get_state("messages")

    if isinstance(messages, list) and len(messages) > 0:
        first_message = messages[0]
        if first_message["role"] == "system":
            first_message["content"] = get_default_system_prompt()
        else:
            messages.insert(0, {
                "role": "system",
                "content": get_default_system_prompt()
            })
    else:
        messages.append({
            "role": "system",
            "content": get_default_system_prompt()
        })
