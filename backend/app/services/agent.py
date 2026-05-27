import os
import re
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from sqlalchemy import Engine, inspect, text
from sqlalchemy.exc import OperationalError, DBAPIError
from app.core.config import settings

# Set environment variables for OpenRouter (OpenAI-compatible)
os.environ["OPENAI_API_KEY"] = settings.openrouter_api_key
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

model = OpenAIModel(settings.ai_model)

# Initialize the agent
agent = Agent(
    model,
    deps_type=Engine,
    system_prompt=(
        "Eres un experto en análisis de datos y SQL. "
        "Tienes acceso de solo lectura a una base de datos PostgreSQL de analítica. "
        "Tu objetivo es responder las preguntas del usuario mediante consultas SQL precisas. "
        "Debes seguir estos pasos:\n"
        "1. Usa 'list_tables' para ver las tablas disponibles si no las conoces.\n"
        "2. Usa 'describe_table' para entender el esquema de las tablas relevantes.\n"
        "3. Genera y ejecuta consultas SQL (solo sentencias SELECT) para obtener los datos.\n"
        "4. Proporciona una respuesta clara y en lenguaje natural en español basada en los resultados.\n\n"
        "Reglas importantes:\n"
        "- Responde siempre en español.\n"
        "- Si no puedes encontrar la información, admítelo.\n"
        "- No inventes datos que no estén en la base de datos.\n"
        "- Siempre verifica los nombres de las columnas antes de realizar consultas complejas.\n"
        "- Solo puedes ejecutar sentencias SELECT."
    )
)

@agent.tool
def list_tables(ctx: RunContext[Engine]) -> list[str]:
    """Listar todas las tablas disponibles en la base de datos de analítica."""
    inspector = inspect(ctx.deps)
    return inspector.get_table_names()

@agent.tool
def describe_table(ctx: RunContext[Engine], table_name: str) -> str:
    """
    Obtener información detallada del esquema de una tabla específica.
    Devuelve los nombres de las columnas y sus tipos.
    """
    inspector = inspect(ctx.deps)
    try:
        columns = inspector.get_columns(table_name)
        if not columns:
            return f"La tabla '{table_name}' no fue encontrada o no tiene columnas."
        
        lines = [f"Tabla: {table_name}"]
        for col in columns:
            lines.append(f"  - {col['name']} ({col['type']})")
        return "\n".join(lines)
    except Exception as e:
        return f"Error al describir la tabla '{table_name}': {str(e)}"

@agent.tool
def execute_read_query(ctx: RunContext[Engine], query: str) -> str:
    """
    Ejecutar una consulta SQL de solo lectura (SELECT).
    Devuelve los resultados formateados como una cadena.
    """
    # 1. Validación estricta y limpieza (Task 1 & 3)
    clean_query = query.strip()
    
    # Bloquear múltiples sentencias (Task 3)
    # Buscamos puntos y coma que no estén al final de la consulta (permitimos uno al final opcional)
    if ";" in clean_query:
        if clean_query.rstrip().count(";") > 1 or (not clean_query.rstrip().endswith(";") and ";" in clean_query):
            return "Error de seguridad: No se permiten múltiples sentencias SQL (uso de ';')."

    upper_query = clean_query.upper()
    
    # Debe empezar con SELECT (Task 1)
    if not upper_query.startswith("SELECT"):
        return "Error de seguridad: Solo se permiten consultas SELECT de solo lectura."

    # Bloquear palabras clave peligrosas (Task 3)
    # Usamos regex para asegurar que son palabras completas y no partes de otras
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE", "GRANT", "REVOKE"]
    for kw in forbidden_keywords:
        if re.search(rf"\b{kw}\b", upper_query):
             return f"Error de seguridad: Se detectó una palabra clave no permitida: {kw}"

    try:
        # Task 2: Execution Timeout (10 segundos)
        with ctx.deps.connect() as conn:
            # Aplicamos el timeout a nivel de ejecución de la sentencia
            # execution_options(timeout=10) es soportado por muchos motores a través de SQLAlchemy
            result = conn.execute(text(query).execution_options(timeout=10))
            rows = result.fetchall()
            if not rows:
                return "La consulta no devolvió resultados."
            
            # Formatear resultados (cabeceras + filas)
            headers = result.keys()
            header_str = " | ".join(headers)
            separator = "-" * len(header_str)
            
            row_lines = []
            for row in rows:
                row_lines.append(" | ".join(str(val) for val in row))
                
            return f"{header_str}\n{separator}\n" + "\n".join(row_lines)
    except OperationalError as e:
        # Errores operacionales como timeouts suelen caer aquí
        error_msg = str(e).lower()
        if "timeout" in error_msg or "expired" in error_msg:
            return "Error: La consulta tomó demasiado tiempo (límite de 10 segundos). Por favor, intenta una consulta más simple."
        return f"Error operacional al ejecutar la consulta: {str(e)}"
    except DBAPIError as e:
        return f"Error de base de datos al ejecutar la consulta: {str(e)}"
    except Exception as e:
        return f"Error inesperado al ejecutar la consulta: {str(e)}"

async def generate_session_title(message: str) -> str:
    """
    Genera un título corto (3-5 palabras) para una sesión de chat basado en el primer mensaje.
    """
    prompt = (
        f"Genera un título muy corto (máximo 5 palabras) en español que resuma esta pregunta: '{message}'. "
        "Devuelve solo el título, sin comillas ni puntos finales."
    )
    try:
        # Usamos el mismo modelo robusto
        title_agent = Agent(model)
        result = await title_agent.run(prompt)
        return result.data.strip()
    except Exception:
        # Fallback si falla la IA
        words = message.split()
        return " ".join(words[:4]) + "..." if len(words) > 4 else message

