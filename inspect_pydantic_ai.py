import pydantic_ai
import inspect

print(f"Pydantic AI version: {pydantic_ai.__version__}")
for name, obj in inspect.getmembers(pydantic_ai):
    if "Result" in name:
        print(f"{name}: {obj}")
