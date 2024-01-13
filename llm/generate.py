from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def generate(model: str,
             messages: list,
             openai_api_key: str,
             stream=True,
             tools=None):
    client = OpenAI(api_key=openai_api_key)
    config = {"model": model}

    if tools:
        config["tools"] = tools
        config["tool_choice"] = "auto"

    if stream is True:
        config["stream"] = True

    response = client.chat.completions.create(
        messages=messages,
        **config
    )

    for chunk in response:
        yield [] if isinstance(chunk, tuple) else chunk.choices
