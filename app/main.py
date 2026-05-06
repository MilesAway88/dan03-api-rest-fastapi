from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db, init_db
from app.models.pedido import Pedido, PedidoDetalle
from app.models.planta import Planta
from app.models.user import User
from app.schemas.pedido import (
    PedidoCreate,
    PedidoDetalleCreate,
    PedidoDetalleResponse,
    PedidoResponse,
)
from app.schemas.planta import PlantaCreate, PlantaResponse
from app.schemas.user import UserCreate, UserResponse

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


# ----------- #
#   Plantas   #
# ----------- #

@app.get(
    "/plantas",
    response_model=list[PlantaResponse],
    tags=["Plantas"],
    summary="Listar todas las plantas",
    description="Retorna una lista de todas las plantas disponibles en MilesPlants"
)
def get_plantas(db: Session = Depends(get_db)):
    return db.query(Planta).all()


@app.get(
    "/planta/{planta_id}",
    response_model=PlantaResponse,
    tags=["Plantas"],
    summary="Buscar planta por ID",
    description="Retorna una planta buscando por su ID. Si no existe, devuelve un error",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Planta no encontrada"}
    }
)
def get_planta_by_id(planta_id: int = Path(example=2), db: Session = Depends(get_db)):
    planta = db.query(Planta).filter(Planta.id == planta_id).first()

    if not planta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Planta no encontrada"
        )
    
    return planta