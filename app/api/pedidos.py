from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.pedido import Pedido, PedidoDetalle
from app.models.planta import Planta
from app.models.user import User
from app.schemas.pedido import PedidoCreate, PedidoResponse

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


# GET todos los pedidos de usuario
@router.get(
    "/",
    response_model=list[PedidoResponse],
    summary="Listar mis pedidos",
    description="Devuelve todos los pedidos realizados por el usuario autenticado"
)
def get_pedidos_usuario(db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    return db.query(Pedido).filter(Pedido.user_id == usuario.id).all()


# GET pedido de usuario por ID
@router.get(
    "/{pedido_id}",
    response_model=PedidoResponse,
    summary="Buscar mi pedido por ID",
    description="Retorna un pedido buscando por su ID, solo si pertenece al usuario autenticado",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Pedido no encontrado o no te pertenece"}
    }
)
def get_pedido_by_id(pedido_id: int = Path(example=8), db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    pedido = db.query(Pedido).filter(
        Pedido.id == pedido_id,
        Pedido.user_id == usuario.id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado o no te pertenece"
        )
    
    return pedido


# POST pedido
@router.post(
    "/",
    response_model=PedidoResponse,
    summary="Crear nuevo pedido",
    description="Crea un pedido validando stock disponible y calculando el total automáticamente",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Stock insuficiente, planta inexistente o lista de detalles vacía"}
    }
)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db), usuario: User = Depends(get_current_user)):
    if not pedido.detalles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El pedido debe contener al menos una planta"
        )
    
    total = Decimal(0)
    plantas_validadas: dict[int, Planta] = {}

    for detalle in pedido.detalles:
        planta = db.query(Planta).filter(Planta.id == detalle.planta_id).first()

        if not planta:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Planta no encontrada"
            )
        
        if bool(planta.stock < detalle.cantidad):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuficiente"
            )
        
        total += planta.precio * Decimal(detalle.cantidad)
        plantas_validadas[planta.id] = planta
    
    nuevo_pedido = Pedido(user_id=usuario.id, estado="pendiente", total=total)
    db.add(nuevo_pedido)
    db.flush() # Genera ID para usarlo en los detalles

    for detalle in pedido.detalles:
        planta = plantas_validadas[detalle.planta_id]

        db.add(PedidoDetalle(
            pedido_id=nuevo_pedido.id,
            planta_id=planta.id,
            cantidad = detalle.cantidad,
            precio_unitario=planta.precio
        ))

        planta.stock -= detalle.cantidad

    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido