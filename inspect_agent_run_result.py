from pydantic_ai.run import AgentRunResult
import inspect

# Let's check the properties of AgentRunResult
for name, obj in inspect.getmembers(AgentRunResult):
    if not name.startswith("__"):
        print(f"{name}: {obj}")
