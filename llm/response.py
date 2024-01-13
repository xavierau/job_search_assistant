import json

from config import AppState


def append_function_call_response(function_call_response):
    messages = AppState.get_instance().get_state("messages", [])

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
    messages = AppState.get_instance().get_state("messages", [])

    messages.append({
        "role": "tool",
        "name": function_call_response.get("name"),
        "content": json.dumps(func_result, indent=4, sort_keys=True, default=str),
        "tool_call_id": function_call_response.get("id"),
    })
