import json
from urllib import error, request


def print_step(step_number: int, phase: str, message: str) -> None:
    print(f"\n===== Step {step_number}: {phase} =====")
    print(message)


def get_weather(city: str) -> str:
    """Return a mock weather result for supported cities."""
    weather_map = {
        "seattle": "24°C and sunny",
        "london": "18°C and cloudy",
        "tokyo": "27°C and humid",
        "new york": "21°C and breezy",
    }
    city_key = city.lower().strip()
    return weather_map.get(city_key, f"I don't have weather data for {city}.")


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to check weather for.",
                    }
                },
                "required": ["city"],
            },
        },
    }
]


def call_ollama_chat(messages: list[dict], model: str = "llama3.2") -> dict:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "tools": tools,
    }

    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        "http://localhost:11434/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
    )

    try:
        with request.urlopen(req, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.URLError as exc:
        raise RuntimeError(
            "Ollama is not running locally. Start it with: ollama serve\n"
            "Also make sure the model is installed: ollama pull llama3.2"
        ) from exc


def run_agent(prompt: str, model: str = "llama3.2") -> str:
    step_number = 1
    print_step(step_number, "Thinking", f"Understanding the user request: '{prompt}'")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful local agent. Use tools when needed to answer accurately.",
        },
        {"role": "user", "content": prompt},
    ]

    step_number += 1
    print_step(step_number, "Calling local model", f"Sending request to Ollama model: {model}")

    try:
        response = call_ollama_chat(messages, model=model)
    except RuntimeError as exc:
        print_step(step_number, "Local model unavailable", str(exc))
        return str(exc)

    assistant_message = response.get("message", {})
    tool_calls = assistant_message.get("tool_calls") or []

    if not tool_calls:
        final_content = assistant_message.get("content") or "No response returned by the model."
        step_number += 1
        print_step(step_number, "Final response", final_content)
        return final_content

    tool_call = tool_calls[0]
    function_name = tool_call.get("function", {}).get("name")
    function_args = tool_call.get("function", {}).get("arguments", {})

    step_number += 1
    print_step(step_number, "Executing tool", f"Tool selected: {function_name} with arguments: {function_args}")

    if function_name == "get_weather":
        city = function_args.get("city", "")
        tool_result = get_weather(city)

        print_step(step_number, "Tool result", f"Retrieved weather for '{city}': {tool_result}")

        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": tool_calls,
        })
        messages.append({
            "role": "tool",
            "content": str(tool_result),
        })

        step_number += 1
        print_step(step_number, "Summarizing", "Sending tool result back to Ollama to create the final answer.")

        final_response = call_ollama_chat(messages, model=model)
        final_answer = final_response.get("message", {}).get("content") or "No final answer returned by the model."

        step_number += 1
        print_step(step_number, "Final response", final_answer)
        return final_answer

    step_number += 1
    final_message = f"Unsupported tool call: {function_name}"
    print_step(step_number, "Final response", final_message)
    return final_message


if __name__ == "__main__":
    user_prompt = "What is the weather in Seattle?"
    print("\nAgent output:")
    print(run_agent(user_prompt))
