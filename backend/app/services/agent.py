import os
from pydantic_ai import Agent, RunContext
from sqlalchemy import Engine, inspect
from app.core.config import settings

# Ensure OpenRouter API key is available in the environment for pydantic-ai
if settings.openrouter_api_key:
    os.environ["OPENROUTER_API_KEY"] = settings.openrouter_api_key
elif "OPENROUTER_API_KEY" not in os.environ:
    # Use a placeholder if not set, to allow the agent to initialize during CI/tests
    os.environ["OPENROUTER_API_KEY"] = "placeholder"

# Initialize the agent
# The "openrouter:" prefix is handled by pydantic-ai's model inference
agent = Agent(
    f"openrouter:{settings.ai_model}",
    deps_type=Engine,
    system_prompt=(
        "You are a database expert assistant. "
        "You have read-only access to a PostgreSQL analytics database. "
        "Your task is to answer user questions by querying the database. "
        "You must follow these steps:\n"
        "1. Use 'list_tables' to see what tables are available.\n"
        "2. Use 'describe_table' to understand the schema of relevant tables.\n"
        "3. Generate and execute SQL queries (only SELECT statements) to get the data.\n"
        "4. Provide a clear, natural language answer based on the query results.\n\n"
        "Always be cautious and verify the schema before assuming column names."
    )
)

@agent.tool
def list_tables(ctx: RunContext[Engine]) -> list[str]:
    """List all available tables in the analytics database."""
    inspector = inspect(ctx.deps)
    return inspector.get_table_names()

@agent.tool
def describe_table(ctx: RunContext[Engine], table_name: str) -> str:
    """
    Get detailed schema information for a specific table.
    Returns column names and their types.
    """
    inspector = inspect(ctx.deps)
    try:
        columns = inspector.get_columns(table_name)
        if not columns:
            return f"Table '{table_name}' not found or has no columns."
        
        lines = [f"Table: {table_name}"]
        for col in columns:
            lines.append(f"  - {col['name']} ({col['type']})")
        return "\n".join(lines)
    except Exception as e:
        return f"Error describing table '{table_name}': {str(e)}"
