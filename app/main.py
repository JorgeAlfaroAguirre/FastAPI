from datetime import datetime
from fastapi import FastAPI
from app.controllers.hello_controller import router as hello_router
from app.controllers.db_controller import router as db_router
from app.controllers.user_controller import router as user_router
from app.controllers.login_controller import router as login_router
from app.controllers.job_offer_controller import router as job_offer_router
from app.controllers.job_application_controller import router as job_application_router
from app.controllers.cv_controller import router as cv_router
from app.controllers.admin_controller import router as admin_router

app = FastAPI(title="BaristaApp API")

# Registro de routers
app.include_router(hello_router)
app.include_router(db_router)
app.include_router(user_router)
app.include_router(login_router)
app.include_router(job_offer_router)
app.include_router(job_application_router)
app.include_router(cv_router)
app.include_router(admin_router)

# Endpoint de salud en la raíz
@app.get("/")
def health():
    return {
        "status": "Servicio activo",
        "Date": datetime.now().isoformat(),
        "service": "BaristaApp API",
        "version": "1.0.0",
        "rutas_disponibles": [
            {"ruta": "/", "método": "GET", "descripción": "Health check y rutas disponibles"},
            {"ruta": "/docs", "método": "GET", "descripción": "Documentación Swagger UI"},
            {"ruta": "/redoc", "método": "GET", "descripción": "Documentación ReDoc"},
            {"ruta": "/miapp", "método": "GET", "descripción": "Endpoint principal de la aplicación"},
            {"ruta": "/db/test-connection", "método": "GET", "descripción": "Probar conexión a la base de datos"},
            {"ruta": "/users", "método": "GET/POST/PUT/DELETE", "descripción": "CRUD de usuarios"},
            {"ruta": "/login", "método": "POST", "descripción": "Autenticación de usuarios"},
            {"ruta": "/job-offers", "método": "GET/POST/PUT/DELETE", "descripción": "CRUD de ofertas de trabajo"},
            {"ruta": "/job-applications", "método": "GET/POST/PUT/DELETE", "descripción": "Gestión de postulaciones"},
            {"ruta": "/cv", "método": "GET/PUT", "descripción": "Gestión de CV de usuarios"}
        ]
    }