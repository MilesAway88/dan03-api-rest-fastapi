from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.pedido import EstadoPedido


class PedidoDetalleBase(BaseModel):
    planta_id: int
    cantidad: int


class PedidoDetalleCreate(PedidoDetalleBase):
    pass


class PedidoDetalleResponse(PedidoDetalleBase):
    id: int
    precio_unitario: float

    model_config = ConfigDict(from_attributes=True)


class PedidoCreate(BaseModel):
    detalles: list[PedidoDetalleCreate]


class PedidoResponse(BaseModel):
    id: int
    user_id: int
    fecha: datetime
    estado: EstadoPedido
    total: float
    detalles: list[PedidoDetalleResponse]

    model_config = ConfigDict(from_attributes=True)