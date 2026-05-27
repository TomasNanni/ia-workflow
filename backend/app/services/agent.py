import os
from pydantic_ai import Agent, RunContext
from sqlalchemy import Engine, inspect, text
from app.core.config import settings

# Ensure OpenRouter API key is available in the environment for pydantic-ai
if settings.openrouter_api_key:
    os.environ["OPENROUTER_API_KEY"] = settings.openrouter_api_key
elif "OPENROUTER_API_KEY" not in os.environ:
    # Use a placeholder if not set, to allow the agent to initialize during CI/tests
    os.environ["OPENROUTER_API_KEY"] = "placeholder"

# Initialize the agent
agent = Agent(
    f"openrouter:{settings.ai_model}",
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
    # Validación básica de seguridad: solo SELECT
    clean_query = query.strip().upper()
    if not clean_query.startswith("SELECT"):
        return "Error: Solo se permiten consultas SELECT de solo lectura."

    try:
        with ctx.deps.connect() as conn:
            result = conn.execute(text(query))
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
    except Exception as e:
        return f"Error al ejecutar la consulta: {str(e)}"

async def generate_session_title(message: str) -> str:
    """
    Genera un título corto (3-5 palabras) para una sesión de chat basado en el primer mensaje.
    """
    prompt = (
        f"Genera un título muy corto (máximo 5 palabras) en español que resuma esta pregunta: '{message}'. "
        "Devuelve solo el título, sin comillas ni puntos finales."
    )
    try:
        # Usamos el mismo modelo pero sin herramientas para una respuesta rápida
        title_agent = Agent(f"openrouter:{settings.ai_model}")
        result = await title_agent.run(prompt)
        return result.data.strip()
    except Exception:
        # Fallback si falla la IA
        words = message.split()
        return " ".join(words[:4]) + "..." if len(words) > 4 else message

