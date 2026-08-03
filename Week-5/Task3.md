# Day 3: Adding Tools & Memory

## 1. Objective & Enhancements
* **Focus:** Extend the agent by adding conversation state (memory) and integrating a second tool.
* **Tools Available:**
  1. `get_weather(location)` — Weather lookup.
  2. `calculate(expression)` — Basic math calculator.
* **Demonstration Goal:** Show how previous conversation turns inform future tool calls.

---

## 2. Agent Code Implementation (Python)

```python
import json
import openai

# --- STEP 1: Define Tools ---
def get_weather(location: str) -> str:
    mock_db = {"london": "15°C, Rainy", "tokyo": "22°C, Sunny", "paris": "19°C, Clear"}
    loc = location.lower()
    temp = mock_db.get(loc, "20°C, Sunny")
    return json.dumps({"location": location, "result": temp})

def calculate(expression: str) -> str:
    try:
        allowed_chars = "0123456789+-*/.() "
        if all(c in allowed_chars for c in expression):
            res = eval(expression)
            return json.dumps({"expression": expression, "result": str(res)})
        return json.dumps({"error": "Invalid expression"})
    except Exception as e:
        return json.dumps({"error": str(e)})

# --- STEP 2: Tool Schemas ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Fetch weather for a given city.",
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
            "description": "Evaluate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string", "description": "Math expression e.g. '22 * 9/5 + 32'"}},
                "required": ["expression"]
            }
        }
    }
]

# --- STEP 3: Agent Class with Conversation Memory ---
class MemoryAgent:
    def __init__(self):
        self.memory = [
            {"role": "system", "content": "You are a helpful multi-tool assistant with short-term memory."}
        ]

    def chat(self, user_input: str):
        self.memory.append({"role": "user", "content": user_input})
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.memory,
            tools=tools,
            tool_choice="auto"
        )
        msg = response.choices[0].message

        if msg.tool_calls:
            self.memory.append(msg)
            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                if name == "get_weather":
                    res = get_weather(args.get("location"))
                elif name == "calculate":
                    res = calculate(args.get("expression"))
                else:
                    res = json.dumps({"error": "Unknown tool"})

                self.memory.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": name,
                    "content": res
                })

            final_resp = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.memory
            )
            final_text = final_resp.choices[0].message.content
            self.memory.append({"role": "assistant", "content": final

        

=== TURN 1 ===
[USER] What is the weather in Tokyo?
[TOOL CALL] get_weather(location="Tokyo")
[OBSERVATION] {"location": "Tokyo", "result": "22°C, Sunny"}
[AGENT RESPONSE] "The weather in Tokyo is currently 22°C and Sunny."

=== TURN 2 (Demonstrating Memory + Multi-Tool Use) ===
[USER] Convert that temperature to Fahrenheit (Formula: C * 9/5 + 32).

[MEMORY RECALL]
Agent reads chat history -> Identifies "that temperature" = 22°C from Turn 1.

[TOOL CALL] calculate(expression="22 * 9/5 + 32")
[OBSERVATION] {"expression": "22 * 9/5 + 32", "result": "71.6"}
[AGENT RESPONSE] "22°C is equivalent to 71.6°F."