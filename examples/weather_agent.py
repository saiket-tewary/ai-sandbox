import json
import os

from dotenv import load_dotenv
from openai import OpenAI, RateLimitError


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing. Add it to the .env file or export it in your shell.")

client = OpenAI(api_key=api_key)


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
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to check the weather for.",
                    }
                },
                "required": ["city"],
            },
        },
    }
]


def run_agent(prompt: str) -> str:
    step_number = 1
    print_step(step_number, "Thinking", f"Understanding the user request: '{prompt}'")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful agent. Use tools when needed to answer the user accurately.",
        },
        {"role": "user", "content": prompt},
    ]

    step_number += 1
    print_step(step_number, "Calling model", "Sending request to the model with the available tools.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
    except RateLimitError:
        print_step(step_number, "API quota exhausted", "OpenAI has no credits remaining. Add credits or use a different model/provider.")
        return "OpenAI quota exhausted. Please add credits or switch to another provider."

    message = response.choices[0].message

    if not message.tool_calls:
        step_number += 1
        print_step(step_number, "Final response", message.content or "No response returned by the model.")
        return message.content or "No response returned by the model."

    tool_call = message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    step_number += 1
    print_step(step_number, "Executing tool", f"Tool selected: {function_name} with arguments: {arguments}")

    if function_name == "get_weather":
        city = arguments["city"]
        tool_result = get_weather(city)

        print_step(step_number, "Tool result", f"Retrieved tool output for '{city}': {tool_result}")

        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [tool_call],
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(tool_result),
        })

        step_number += 1
        print_step(step_number, "Summarizing", "Sending the tool result back to the model to generate the final answer.")

        try:
            final_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
            )
        except RateLimitError:
            print_step(step_number, "API quota exhausted", "The second model call was rejected because the account has no credits remaining.")
            return "OpenAI quota exhausted. Please add credits or use a different model/provider."

        final_answer = final_response.choices[0].message.content

        step_number += 1
        print_step(step_number, "Final response", final_answer or "No final answer returned by the model.")
        return final_answer or "No final answer returned by the model."

    step_number += 1
    print_step(step_number, "Final response", f"Unsupported tool call: {function_name}")
    return f"Unsupported tool call: {function_name}"


if __name__ == "__main__":
    user_prompt = "What is the weather in Seattle?"
    print("\nAgent output:")
    print(run_agent(user_prompt))
