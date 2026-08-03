# Day 5: Failure Modes & Guardrails

## 1. Objective & Overview
* **Focus:** Identify common ways AI agents fail in production and implement defensive guardrails to prevent incorrect, unsafe, or endless execution behavior.
* **Failure Modes Addressed:**
  1. **Infinite Execution Loop / Tool Thrashing:** Agent stuck repeatedly calling tools when an answer isn't found.
  2. **Unsafe / Insecure Code Execution:** User or LLM attempting arbitrary code or injection inside tool parameters.
  3. **Hallucinated or Invalid Tool Arguments:** Tool failing due to improper arguments passed by the LLM.

---

## 2. Guardrails Implementation & Agent Code (Python)

```python
import json
import re
import openai

# --- GUARDRAIL 1: Input Validation & Sanitization ---
def safe_calculator(expression: str) -> str:
    """Guardrail against arbitrary code execution/eval injection."""
    allowed_pattern = r"^[0-9\+\-\*\/\.\(\)\s]+$"
    
    if not re.match(allowed_pattern, expression):
        return json.dumps({
            "status": "error",
            "message": "Security Alert: Expression contains unauthorized characters."
        })
    
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return json.dumps({"status": "success", "result": str(result)})
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Calculation failed: {str(e)}"})


def get_weather(location: str) -> str:
    """Mock weather tool with input verification."""
    if not isinstance(location, str) or len(location.strip()) == 0:
        return json.dumps({"status": "error", "message": "Invalid location argument."})
    
    return json.dumps({"status": "success", "location": location, "temperature": "22°C"})


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Fetch current weather for a city.",
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
            "name": "safe_calculator",
            "description": "Perform mathematical calculations safely.",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"]
            }
        }
    }
]


# --- GUARDRAILED AGENT ENGINE ---
class GuardrailedAgent:
    def __init__(self, max_iterations: int = 3):
        # GUARDRAIL 2: Loop Limit Ceiling
        self.max_iterations = max_iterations
        self.messages = [
            {
                "role": "system",
                "content": "You are a safe AI agent. Adhere to security rules and stop execution if a tool returns an error."
            }
        ]

    def run(self, user_prompt: str):
        self.messages.append({"role": "user", "content": user_prompt})
        iteration_count = 0

        while iteration_count < self.max_iterations:
            iteration_count += 1
            
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
                tools=tools,
                tool_choice="auto"
            )
            msg = response.choices[0].message
            self.messages.append(msg)

            if not msg.tool_calls:
                return msg.content

            for tool_call in msg.tool_calls:
                name = tool_call.function.name
                
                # GUARDRAIL 3: Schema & Argument Parsing Validation
                try:
                    args = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    tool_output = json.dumps({"status": "error", "message": "Malformed JSON arguments."})
                else:
                    if name == "safe_calculator":
                        tool_output = safe_calculator(args.get("expression", ""))
                    elif name == "get_weather":
                        tool_output = get_weather(args.get("location", ""))
                    else:
                        tool_output = json.dumps({"status": "error", "message": "Unknown tool called."})

                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": name,
                    "content": tool_output
                })

        return f"[GUARDRAIL TRIGGERED]: Max iteration limit ({self.max_iterations}) reached. Halting execution to prevent infinite loop."


# --- RUN TEST CASES ---
if __name__ == "__main__":
    agent = GuardrailedAgent(max_iterations=3)
    prompt = "Calculate: __import__('os').system('ls')"
    print(agent.run(prompt))


=== TEST CASE: CODE INJECTION GUARDRAIL ===

[USER INPUT]
Calculate: __import__('os').system('ls')

[AGENT TOOL CALL]
safe_calculator(expression="__import__('os').system('ls')")

[GUARDRAIL TRIGGERED: INPUT SANITIZATION]
Pattern validation failed -> Unauthorized characters detected.

[TOOL OBSERVATION]
{"status": "error", "message": "Security Alert: Expression contains unauthorized characters."}

[FINAL AGENT RESPONSE]
"I cannot execute that calculation because it contains unauthorized characters or security risks."  