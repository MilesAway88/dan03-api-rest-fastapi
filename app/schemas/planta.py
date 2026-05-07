from pydantic import BaseModel, ConfigDict

from app.models.planta import TipoPlanta


class PlantaBase(BaseModel):
    tipo: TipoPlanta
    nombre_comun: str
    nombre_latin: str
    precio: float
    stock: int


class PlantaCreate(PlantaBase):
    pass


class PlantaResponse(PlantaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)