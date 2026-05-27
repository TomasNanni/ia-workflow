from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
import os
import asyncio

async def test():
    model = OpenAIModel('gpt-3.5-turbo') # Doesn't matter, we just want to see the result object attributes
    agent = Agent(model)
    print(f"Agent result type: {type(agent)}")
    
    # Let's see the attributes of the result class if possible
    from pydantic_ai.result import RunResult
    print(f"RunResult attributes: {dir(RunResult)}")

if __name__ == "__main__":
    asyncio.run(test())
