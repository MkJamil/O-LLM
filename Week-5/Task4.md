# Day 4: Planning & Task Decomposition

## 1. Objective & Scenario
* **Focus:** Demonstrate how an agent breaks down a high-level, multi-step goal into sub-tasks, plans their execution, and handles intermediate tool outputs.
* **Complex Task Prompt:** *"Research the current weather in Tokyo, calculate what 22°C is in Fahrenheit, and compile a final summary report."*
* **Required Sub-tasks (Decomposition):**
  1. Fetch Tokyo weather data (`get_weather`).
  2. Parse the extracted Celsius temperature.
  3. Execute conversion math (`calculate`).
  4. Aggregate findings into a final user report.

---

## 2. Agent Code Implementation (Python)

```python
import json
import openai

# --- STEP 1: Tools & Decomposition Registry ---
def get_weather(location: str) -> str:
    """Fetches weather data."""
    mock_db = {"tokyo": "22°C", "london": "15°C", "paris": "18°C"}
    temp = mock_db.get(location.lower(), "20°C")
    return json.dumps({"location": location, "temperature_celsius": temp})

def calculate(expression: str) -> str:
    """Executes mathematical calculations."""
    try:
        allowed = "0123456789+-*/.() "
        if all(c in allowed for c in expression):
            res = eval(expression)
            return json.dumps({"expression": expression, "result": str(res)})
        return json.dumps({"error": "Invalid characters"})
    except Exception as e:
        return json.dumps({"error": str(e)})

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical evaluation.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"]
            }
        }
    }
]

# --- STEP 2: Planning & Execution Agent ---
class PlanningAgent:
    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a planning AI agent. When given a complex goal, break it down "
                    "into sequential steps. Reason out your plan before invoking tools."
                )
            }
        ]

    def execute_plan(self, user_goal: str):
        self.messages.append({"role": "user", "content": user_goal})
        
        while True:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
                tools=tools,
                tool_choice="auto"
            )
            msg = response.choices[0].message
            self.messages.append(msg)

            # Check if agent calls tools or outputs final answer
            if msg.tool_calls:
                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    if name == "get_weather":
                        out = get_weather(args.get("location"))
                    elif name == "calculate":
                        out = calculate(args.get("expression"))
                    else:
                        out = json.dumps({"error": "Unknown tool"})

                    self.messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": name,
                        "content": out
                    })
            else:
                # Goal reached (Final Summary Output)
                return msg.content


# --- RUN DECOMPOSITION DEMO ---
if __name__ == "__main__":
    agent = PlanningAgent()
    prompt = "Find the current weather in Tokyo, convert the Celsius temperature to Fahrenheit using (C * 9/5) + 32, and give me a summary."
    print(agent.execute_plan(prompt))


=== AGENT TASK DECOMPOSITION TRACE ===

[GOAL] 
Find current weather in Tokyo, convert its Celsius temperature to Fahrenheit, and summarize.

--- STEP 1: INITIAL PLANNING & TOOL CHOICE ---
[THOUGHT] To achieve this goal, I need to break it down:
  1. Fetch weather in Tokyo to extract the temperature in Celsius.
  2. Take the extracted value and run the formula (C * 9/5) + 32 via calculator.
  3. Compile the final results.

[ACTION] get_weather(location="Tokyo")
[OBSERVATION] {"location": "Tokyo", "temperature_celsius": "22°C"}

--- STEP 2: DEPENDENT STEP EXECUTION ---
[THOUGHT] The weather in Tokyo is 22°C. Now I must calculate: (22 * 9/5) + 32.
[ACTION] calculate(expression="(22 * 9/5) + 32")
[OBSERVATION] {"expression": "(22 * 9/5) + 32", "result": "71.6"}

--- STEP 3: SYNTHESIS & FINAL OUTPUT ---
[THOUGHT] Both sub-tasks complete. Preparing final summary report.

[FINAL AGENT RESPONSE]
### Tokyo Weather & Conversion Summary
- **Location:** Tokyo
- **Temperature (Celsius):** 22°C
- **Temperature (Fahrenheit):** 71.6°F

The current weather in Tokyo is 22°C, which is equal to 71.6°F.