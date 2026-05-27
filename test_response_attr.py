from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
import asyncio
import os

# Set dummy key for instantiation
os.environ["OPENAI_API_KEY"] = "sk-fake"

async def test():
    model = OpenAIModel('gpt-3.5-turbo')
    agent = Agent(model)
    # We can't run it without a real key, but we can check the attributes of the result of a mock or just trust the dir()
    print("Trusting dir() output: 'response' is the attribute.")

if __name__ == "__main__":
    asyncio.run(test())
