# Day 2: Tool Use / Function Calling

## 1. Objective & Setup
* **Focus:** Build a simple agent capable of dynamically invoking a single external tool based on natural language user prompts.
* **Tool Name:** `get_weather(location)`
* **Scenario:** The user asks for weather information. The agent identifies the missing data, calls the function, and uses the observation to answer.

---

## 2. Agent Code Implementation (Python)

```python
import json
import openai

# --- STEP 1: External Tool Implementation ---
def get_weather(location: str) -> str:
    """Mock external Weather API call."""
    mock_weather_db = {
        "london": {"temperature": "15°C", "condition": "Cloudy"},
        "tokyo": {"temperature": "22°C", "condition": "Sunny"},
        "new york": {"temperature": "18°C", "condition": "Rainy"}
    }
    
    city = location.lower()
    if city in mock_weather_db:
        data = mock_weather_db[city]
        return json.dumps({"location": location, "temperature": data["temperature"], "condition": data["condition"]})
    else:
        return json.dumps({"location": location, "temperature": "20°C", "condition": "Clear"})


# --- STEP 2: Function Calling Schema ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather details for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g. London, Tokyo"
                    }
                },
                "required": ["location"]
            }
        }
    }
]


# --- STEP 3: Agent Runner ---
def run_single_tool_agent(user_prompt: str):
    messages = [{"role": "user", "content": user_prompt}]
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        messages.append(response_message)
        
        for tool_call in tool_calls:
            if tool_call.function.name == "get_weather":
                args = json.loads(tool_call.function.arguments)
                tool_output = get_weather(location=args.get("location"))
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_weather",
                    "content": tool_output
                })
        
        final_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final_response.choices[0].message.content

    return response_message.content


# --- RUN DEMO ---
if __name__ == "__main__":
    prompt = "What is the weather like in Tokyo right now?"
    result = run_single_tool_agent(prompt)
    print("Agent Output:", result)


=== EXECUTION TRACE ===

[USER INPUT]
What is the weather like in Tokyo right now?

[AGENT THOUGHT]
The user is asking for weather information in Tokyo. I need to invoke the `get_weather` tool.

[TOOL CALL]
get_weather(location="Tokyo")

[OBSERVATION]
{"location": "Tokyo", "temperature": "22°C", "condition": "Sunny"}

[AGENT RESPONSE]
The current weather in Tokyo is 22°C and Sunny.