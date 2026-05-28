import asyncio
import os
import sys
from sqlalchemy import create_engine

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.services.agent import agent, list_tables, describe_table, execute_read_query
from app.core.config import settings
from pydantic_ai import RunContext

from unittest.mock import MagicMock

async def test_agent_tools():
    engine = create_engine("sqlite:///:memory:")
    # Create a dummy table
    with engine.connect() as conn:
        from sqlalchemy import text
        conn.execute(text("CREATE TABLE test_table (id INTEGER, name TEXT)"))
        conn.execute(text("INSERT INTO test_table VALUES (1, 'test')"))
        conn.commit()
    
    ctx = MagicMock()
    ctx.deps = engine
    
    print("Testing list_tables...")
    tables = list_tables(ctx)
    print(f"Tables: {tables}")
    assert "test_table" in tables
    
    print("Testing describe_table...")
    description = describe_table(ctx, "test_table")
    print(f"Description:\n{description}")
    assert "id" in description
    assert "name" in description
    
    print("Testing execute_read_query...")
    result = execute_read_query(ctx, "SELECT * FROM test_table")
    print(f"Result:\n{result}")
    assert "test" in result
    
    print("Testing security validation (non-SELECT)...")
    result = execute_read_query(ctx, "DELETE FROM test_table")
    print(f"Result: {result}")
    assert "Error: Solo se permiten consultas SELECT" in result

    print("All tool tests passed!")

if __name__ == "__main__":
    asyncio.run(test_agent_tools())
