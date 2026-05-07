from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# String de conexión
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# Motor de BD
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para modelos
Base = declarative_base()

# Generador de dependencias para BD
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Inicialización de tablas
def init_db():
    Base.metadata.create_all(bind=engine)