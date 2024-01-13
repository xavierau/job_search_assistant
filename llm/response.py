import json

import streamlit


def append_function_call_response(function_call_response):
    messages = streamlit.session_state.messages or []

    messages.append({
        "content": "",
        "role": "assistant",
        "tool_calls": [{
            "id": function_call_response.get("id"),
            "type": "function",
            "function": {
                "name": function_call_response.get("name"),
                "arguments": function_call_response.get("arguments"),
            }
        }]
    })


def append_tool_response(function_call_response, func_result):
    messages = streamlit.session_state.messages or []

    messages.append({
        "role": "tool",
        "name": function_call_response.get("name"),
        "content": json.dumps(func_result, indent=4, sort_keys=True, default=str),
        "tool_call_id": function_call_response.get("id"),
    })
