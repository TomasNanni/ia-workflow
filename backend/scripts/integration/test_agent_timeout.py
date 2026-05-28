import sys
import os
# Añadir el directorio raíz al path para poder importar app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from sqlalchemy import create_engine
from pydantic_ai import RunContext
from app.services.agent import execute_read_query
import time

# Crear un motor de SQLite para la prueba
engine = create_engine("sqlite:///:memory:")

# Mock RunContext
class MockContext:
    def __init__(self, deps):
        self.deps = deps

ctx = MockContext(engine)

def test_timeout():
    print("--- Test de Timeout ---")
    
    # Consulta pesada que empieza con SELECT
    query = """
    SELECT a.x FROM 
    (WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt LIMIT 10000) SELECT x FROM cnt) a 
    CROSS JOIN 
    (WITH RECURSIVE cnt(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM cnt LIMIT 10000) SELECT x FROM cnt) b 
    LIMIT 1;
    """
    
    print(f"Ejecutando consulta pesada (timeout esperado en 10s)...")
    start_time = time.time()
    result = execute_read_query(ctx, query)
    end_time = time.time()
    
    print(f"Resultado: {result[:200]}...")
    print(f"Tiempo transcurrido: {end_time - start_time:.2f} segundos")
    
    if "timeout" in result.lower() or "demasiado tiempo" in result.lower():
        print("✅ Timeout detectado correctamente")
    else:
        print("❌ Timeout NO detectado (la consulta terminó antes o falló por otra razón)")

if __name__ == "__main__":
    test_timeout()
