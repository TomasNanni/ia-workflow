from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import inspect
from app.core.database import analytics_engine
from app.services.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/schema")
def get_schema(current_user: User = Depends(get_current_user)):
    """
    Obtener el esquema de la base de datos de analítica (tablas y columnas).
    """
    if not analytics_engine:
        raise HTTPException(status_code=500, detail="El motor de base de datos de analítica no está configurado")
    
    try:
        inspector = inspect(analytics_engine)
        schema_info = []
        
        for table_name in inspector.get_table_names():
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    "name": column["name"],
                    "type": str(column["type"])
                })
            
            schema_info.append({
                "name": table_name,
                "columns": columns
            })
            
        return schema_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el esquema: {str(e)}")
