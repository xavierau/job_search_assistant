import streamlit

from helpers import stows
from llm.generate import generate

cover_letter_writer_schema = {
    "type": "function",
    "function": {
        "name": "cover_letter_writer",
        "description": "Use this function to create a cover letter for job application.",
        "parameters": {
            "type": "object",
            "properties": {
                "job_title": {
                    "type": "string",
                    "description": "job title or name for the job post",
                },
                "job_description": {
                    "type": "string",
                    "description": "the detail of the job opening. e.g. company name, requirement, resiponsibility, application reference number etc.",
                },
            },
            "required": ["job_title", "job_description"],
        },
    },
}


def cover_letter_writer(job_title: str,
                        job_description: str, ):
    user_info_dict = streamlit.session_state.user_profile

    system_prompt = f""" You are a great cover letter writer. Following principles will help you to write a great cover letter.
        1. Focus it on the future. 
        The cover letter should focus on the future and what you want to do.
        
        2. Open strong. 
        Lead with a strong opening sentence. “Start with the punch line — why this job is exciting to you and what you bring to the table.
        
        3. Emphasize your personal value. 
        Show that you know what the company does and some of the challenges it faces. Then talk about you to meet those needs; perhaps explain how you solved a similar problem in the past or share a relevant accomplishment.
        
        4. Convey enthusiasm. 
        Make it clear why you want the position. “Enthusiasm conveys personality,”  Don’t bother applying if you’re not excited about some aspect of the company or role.
        
        5. Keep it short. 
        It should be brief enough that someone can read it at a glance.” You do have to cover a lot of ground — but you should do it succinctly.
        """

    user_message_content = f"Can you create a cover letter for me about the following job?\nJob Title:\n{job_title}\nJob Description:\n{job_description}\n================================"

    if len(user_info_dict.items()) > 0:
        user_info = "\n".join([f"{stows(key)} {val}" for key, val in user_info_dict.items()])
        user_message_content += f"\nBelow is the personal info about the myself.\n{user_info}\n================================"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message_content}
    ]

    content = ""
    for response in generate(model=streamlit.session_state.openai_model,
                             messages=messages,
                             openai_api_key=streamlit.session_state.openai_api_key):
        if len(response) > 0:
            content += response[0].delta.content or ""

    return {
        'status': "completed",
        "cover_letter": content
    }
