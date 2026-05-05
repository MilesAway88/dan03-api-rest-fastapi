import enum

from sqlalchemy import (
    Column,
    Enum,
    Integer,
    Numeric,
    String,
)

from app.core.database import Base


class TipoPlanta(str, enum.Enum):
    ARBUSTO = "arbusto"
    SUCULENTA = "suculenta"
    FRUTAL = "frutal"
    ENREDADERA = "enredadera"


class Planta(Base):
    __tablename__ = "plantas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(Enum(TipoPlanta), nullable=False)
    nombre_comun = Column(String(100), nullable=False)
    nombre_latin = Column(String(100), nullable=False)
    precio = Column(Numeric(8, 2), nullable=False)
    stock = Column(Integer, default=0, nullable=False)