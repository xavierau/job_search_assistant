import json
from datetime import datetime

import streamlit

from llm.generate import generate
from llm.prompts import get_default_system_prompt
from llm.response import append_function_call_response, append_tool_response


def stows(s):
    return s.replace("_", " ").title()


def init_session_vars():
    if "track_state" not in streamlit.session_state:
        streamlit.session_state.track_state = datetime.now()

    if "featured_jobs" not in streamlit.session_state:
        streamlit.session_state.featured_jobs = []

    if "messages" not in streamlit.session_state:
        streamlit.session_state.messages = [{
            "role": "system",
            "content": get_default_system_prompt()
        }]

    if "openai_model" not in streamlit.session_state:
        streamlit.session_state.openai_model = "gpt-3.5-turbo-1106"

    if "openai_api_key" not in streamlit.session_state:
        streamlit.session_state.openai_api_key = None

    if "user_profile" not in streamlit.session_state:
        streamlit.session_state.user_profile = {}


def execute_functions(_tools, function_calls):
    funcs = {t.get("name"): t.get("func") for t in _tools}
    for function_call in function_calls:
        func = funcs.get(function_call.get('name'))
        if func:
            append_function_call_response(function_call)
            func_args = json.loads(function_call.get('arguments'))
            func_result = func(**func_args)
            append_tool_response(function_call, func_result)

    function_calls.clear()
    return function_calls


def update_function_calls(tool_calls, function_calls=[], message_placeholder=None):
    tool_call = tool_calls[0]

    if tool_call.id:
        function_calls.append({
            "id": tool_call.id,
            "name": tool_call.function.name,
            "arguments": ""
        })
        message_placeholder.text(f"Calling plugin: {tool_call.function.name}" + " ▌")
    else:
        function_call = function_calls[-1]
        function_call['arguments'] += tool_call.function.arguments

    return function_calls


def update_outputs(response, msg, mp):
    response += msg or ""
    mp.markdown(response + " ▌")
    return response


def call(messages, tools, message_placeholder, response_message="", function_calls=[]):
    for response in generate(
            model=streamlit.session_state.openai_model,
            messages=messages,
            openai_api_key=streamlit.session_state.openai_api_key,
            tools=[t.get("schema") for t in tools]):
        if len(response) > 0:
            if response[0].finish_reason == 'tool_calls':
                function_calls = execute_functions(tools, function_calls)
                response_message = call(messages, tools, message_placeholder, response_message, function_calls)

            elif response[0].delta.tool_calls:
                function_calls = update_function_calls(response[0].delta.tool_calls, function_calls,
                                                       message_placeholder)

            elif response[0].delta.content:
                response_message = update_outputs(response_message, response[0].delta.content, mp=message_placeholder)

    return response_message
