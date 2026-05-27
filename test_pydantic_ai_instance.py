from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel
import asyncio

async def test():
    # TestModel doesn't need an API key
    model = TestModel()
    agent = Agent(model)
    result = await agent.run("hello")
    print(f"Result type: {type(result)}")
    print(f"Result attributes: {dir(result)}")
    try:
        print(f"Result data: {result.data}")
    except Exception as e:
        print(f"Error accessing .data: {e}")
    try:
        print(f"Result output: {result.output}")
    except Exception as e:
        print(f"Error accessing .output: {e}")
    try:
        print(f"Result response: {result.response}")
    except Exception as e:
        print(f"Error accessing .response: {e}")

if __name__ == "__main__":
    asyncio.run(test())
