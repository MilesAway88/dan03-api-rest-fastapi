from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.planta import Planta
from app.schemas.planta import PlantaCreate, PlantaResponse

router = APIRouter(tags=["Plantas"])

@router.get(
    "/plantas",
    response_model=list[PlantaResponse],
    summary="Listar todas las plantas",
    description="Retorna una lista de todas las plantas disponibles en MilesPlants"
)
def get_plantas(db: Session = Depends(get_db)):
    return db.query(Planta).all()


@router.get(
    "/planta/{planta_id}",
    response_model=PlantaResponse,
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


@router.post(
    "/plantas",
    response_model=PlantaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva planta",
    description="Añade una nueva planta al catálogo. Valida automáticamente el cuerpo de la petición",
)
def create_planta(planta: PlantaCreate, db: Session = Depends(get_db)):
    # Para modelos más grandes
    # planta_db = Planta(**planta.model_dump())

    planta_db = Planta(
        tipo=planta.tipo,
        nombre_comun=planta.nombre_comun,
        nombre_latin=planta.nombre_latin,
        precio=planta.precio,
        stock=planta.stock,
    )

    db.add(planta_db)
    db.commit()
    db.refresh(planta_db)
    return planta_db