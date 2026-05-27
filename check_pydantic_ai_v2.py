try:
    from pydantic_ai.result import AgentRunResult
    print(f"AgentRunResult attributes: {dir(AgentRunResult)}")
except Exception as e:
    print(f"Error importing AgentRunResult: {e}")

try:
    from pydantic_ai.result import RunResult
    print(f"RunResult attributes: {dir(RunResult)}")
except Exception as e:
    print(f"Error importing RunResult: {e}")
