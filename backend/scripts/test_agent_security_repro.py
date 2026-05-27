import sys
import os
# Añadir el directorio raíz al path para poder importar app
sys.path.append(os.getcwd())

from sqlalchemy import create_engine
from pydantic_ai import RunContext
from app.services.agent import execute_read_query

# Crear un motor de SQLite en memoria para la prueba
engine = create_engine("sqlite:///:memory:")

# Mock RunContext
class MockContext:
    def __init__(self, deps):
        self.deps = deps

ctx = MockContext(engine)

def test_security():
    print("--- Test de Seguridad ---")
    
    queries = [
        "SELECT * FROM users; DROP TABLE sessions;",
        "SELECT * FROM users --; DROP TABLE sessions;",
        "INSERT INTO users (name) VALUES ('hacker'); SELECT * FROM users;",
        "UPDATE users SET role = 'admin';",
        "SELECT (SELECT DELETE FROM logs);"
    ]
    
    for q in queries:
        print(f"Probando: {q}")
        result = execute_read_query(ctx, q)
        print(f"Resultado: {result}")
        print("-" * 20)

if __name__ == "__main__":
    test_security()
