from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.pedidos import router as pedidos_router
from app.api.plantas import router as plantas_router
from app.core.database import init_db

openapi_tags = [
    {
        "name": "Plantas",
        "description": "Operaciones para consultar plantas."
    },
    {
        "name": "Pedidos",
        "description": "Operaciones para gestionar pedidos."
    },
    {
        "name": "Usuarios",
        "description": "Operaciones para registrar y loguear usuarios."
    },
]


# Se ejecuta al iniciar el servidor
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("Prueba de conexión OK")
    yield


app = FastAPI(
    title="MilesPlantsAPI",
    summary="API para consultar y gestionar reservas de plantas.",
    description="""
        Esta API REST permite gestionar la compra de plantas de "MilesPlants".
        Permite consultar plantas, comprobar su disponibilidad y administrar pedidos tras autenticación de usuario.
    """,
    version="0.1.0",
    contact={
        "name": "Milena Sánchez Navarro",
        "email": "milenasanchez@paucasesnovescifp.cat",
    },
    license_info={"name": "CC BY"},
    openapi_tags=openapi_tags,
    lifespan=lifespan
)


# Registro de routers
app.include_router(plantas_router)
app.include_router(auth_router)
app.include_router(pedidos_router)