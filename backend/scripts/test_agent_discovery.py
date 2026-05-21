import sys
import os
from dataclasses import dataclass
from typing import Any

# Add backend to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.agent import agent, list_tables, describe_table
from app.core.database import analytics_engine

@dataclass
class MockContext:
    deps: Any
    retry: int = 0
    usage: Any = None

def test_discovery():
    print("Testing Agent Schema Discovery Tools...")
    
    if not analytics_engine:
        print("Error: Analytics engine not configured. Set ANALYTICS_DB_URL in .env")
        sys.exit(1)

    # 1. Test tools directly with MockContext
    print("\n[1/2] Testing tools directly...")
    mock_ctx = MockContext(deps=analytics_engine)
    
    try:
        # Test list_tables
        print("Running list_tables...")
        tables = list_tables(mock_ctx)
        print(f"Tables found: {tables}")
        
        # Verify common tables from seed script
        expected_tables = ["customers", "products", "sales"]
        for table in expected_tables:
            if table in tables:
                print(f"✅ Found table: {table}")
            else:
                print(f"❌ Missing table: {table} (Might be OK if DB not seeded yet)")

        # Test describe_table
        if tables:
            test_table = tables[0]
            print(f"\nDescribing '{test_table}' table...")
            description = describe_table(mock_ctx, test_table)
            print(f"Description:\n{description}")
            if test_table in description and "Table:" in description:
                 print(f"✅ describe_table tool works for '{test_table}'")
            else:
                 print(f"❌ describe_table output looks incorrect for '{test_table}'")
        
    except Exception as e:
        print(f"❌ Error during tool testing: {e}")
        import traceback
        traceback.print_exc()

    # 2. Test agent integration (Programmatic run)
    print("\n[2/2] Testing agent integration (stateless)...")
    try:
        # We use a simple prompt that should trigger tool use or just basic response
        # To avoid spending many tokens, we'll ask it to just use the tool once.
        print("Asking agent to list tables...")
        result = agent.run_sync("Please list the available tables in the database.", deps=analytics_engine)
        print(f"Agent Response: {result.data}")
        print("✅ Agent run successful!")
        
    except Exception as e:
        print(f"❌ Error during agent run: {e}")
        # Note: This might fail if the API key is invalid or model is unavailable
        # But if it fails because of tool calling, it's a bug in our implementation.

if __name__ == "__main__":
    test_discovery()
