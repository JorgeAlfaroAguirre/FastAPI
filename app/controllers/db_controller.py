from fastapi import APIRouter, HTTPException
from sqlmodel import text
from app.services.db.sql_server_connection import get_session

router = APIRouter(prefix="/db", tags=["Database"])

@router.get("/test-connection")
def test_db_connection():
    """
    Endpoint para probar la conexión a la base de datos SQL Server.
    Ejecuta una consulta simple y retorna el resultado.
    """
    try:
        # Obtener una sesión de la base de datos
        session_generator = get_session()
        session = next(session_generator)

        # Ejecutar una consulta simple para verificar la conexión
        result = session.exec(text("SELECT 1 AS test")).first()

        # Cerrar la sesión
        try:
            next(session_generator)
        except StopIteration:
            pass  # La sesión se cierra automáticamente

        return {
            "status": "success",
            "message": "Conexión a la base de datos exitosa",
            "database": "SQL Server",
            "test_query_result": result[0] if result else None
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Error al conectar con la base de datos",
                "error": str(e)
            }
        )