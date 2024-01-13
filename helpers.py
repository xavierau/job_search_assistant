import json

from config import AppState, Config
from llm.generate import generate
from llm.prompts import get_default_system_prompt
from llm.response import append_function_call_response, append_tool_response


def stows(s):
    return s.replace("_", " ").title()


def init_session_vars():
    if AppState.get_instance().length() == 0:
        AppState.get_instance().set({
            "featured_jobs": [],
            "messages": [{
                "role": "system",
                "content": get_default_system_prompt()
            }],
        })

    if Config.get_instance().length() == 0:
        Config.get_instance().set({
            "openai_model": "gpt-3.5-turbo-1106",
            "openai_api_key": None,
            "user_profile": {},
        })


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
    for i, call in enumerate(tool_calls):
        for j in range(i - len(function_calls) + 1):
            function_calls.append({
                "id": None,
                "name": None,
                "arguments": ""
            })

        if tool_calls[i].function.name:
            function_name = tool_calls[i].function.name
            function_calls[i]['id'] = tool_calls[i].id
            function_calls[i]['name'] = function_name
            message_placeholder.text(f"Calling plugin: {function_name}" + " ▌")
        function_calls[i]['arguments'] += tool_calls[i].function.arguments

    return function_calls


def update_outputs(response, msg, mp):
    response += msg or ""
    mp.markdown(response + " ▌")
    return response


def call(messages, tools, message_placeholder, response_message="", function_calls=[]):
    for response in generate(
            model=Config.get_instance().get_config("openai_model"),
            messages=messages,
            openai_api_key=Config.get_instance().get_config("openai_api_key"),
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
