import sys
from datetime import datetime, timezone
from pathlib import Path

# Añadir la raíz del proyecto al PATH para importar app
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.core.security import get_password_hash
from app.models.pedido import EstadoPedido, Pedido, PedidoDetalle
from app.models.planta import Planta, TipoPlanta
from app.models.user import User


def seed_db():
    # Crear tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Crear plantas (solo si no hay ninguna)
        if db.query(Planta).count() == 0:
            plantas = [
                Planta(tipo=TipoPlanta.ARBUSTO, nombre_comun="Boj común", nombre_latin="Buxus sempervirens", precio=12.50, stock=5),
                Planta(tipo=TipoPlanta.ARBUSTO, nombre_comun="Galán de noche", nombre_latin="Cestrum nocturnum", precio=14.95, stock=8),
                Planta(tipo=TipoPlanta.ARBUSTO, nombre_comun="Hibisco", nombre_latin="Hibiscus rosa-sinensis", precio=8.95, stock=30),
                Planta(tipo=TipoPlanta.ARBUSTO, nombre_comun="Kalanchoe", nombre_latin="Kalanchoe blossfeldiana", precio=9.50, stock=50),
                Planta(tipo=TipoPlanta.SUCULENTA, nombre_comun="Collar de corazone", nombre_latin="Ceropegia woodii", precio=15.50, stock=10),
                Planta(tipo=TipoPlanta.SUCULENTA, nombre_comun="Crásula", nombre_latin="Crassula capitella", precio=18.50, stock=33),
                Planta(tipo=TipoPlanta.SUCULENTA, nombre_comun="Haworthia", nombre_latin="Haworthia retusa", precio=5.50, stock=97),
                Planta(tipo=TipoPlanta.SUCULENTA, nombre_comun="Árbol de Jade", nombre_latin="Portulacaria afra", precio=8.00, stock=210),
                Planta(tipo=TipoPlanta.FRUTAL, nombre_comun="Aguacatero", nombre_latin="Persea americana", precio=25.00, stock=45),
                Planta(tipo=TipoPlanta.FRUTAL, nombre_comun="Algarrobo", nombre_latin="Ceratonia siliqua", precio=11.50, stock=82),
                Planta(tipo=TipoPlanta.FRUTAL, nombre_comun="Granado", nombre_latin="Punica granatum", precio=13.95, stock=56),
                Planta(tipo=TipoPlanta.FRUTAL, nombre_comun="Higuera", nombre_latin="Ficus carica", precio=14.50, stock=71),
                Planta(tipo=TipoPlanta.ENREDADERA, nombre_comun="Hiedra de Canarias", nombre_latin="Hedera canariensis", precio=23.00, stock=20),
                Planta(tipo=TipoPlanta.ENREDADERA, nombre_comun="Buganvilla", nombre_latin="Bougainvillea glabra", precio=19.50, stock=66),
                Planta(tipo=TipoPlanta.ENREDADERA, nombre_comun="Jazmín", nombre_latin="Jasminum officinale", precio=9.75, stock=18),
                Planta(tipo=TipoPlanta.ENREDADERA, nombre_comun="Flor de la pasión", nombre_latin="Passiflora incarnata", precio=25.75, stock=59),
            ]
            db.add_all(plantas)
            db.commit()
        
        # Crear usuario (solo si no existe)
        if db.query(User).filter(User.email == "profesor@test.com").first() is None:
            usuario = User(
                nombre="Test",
                email="test@test.com",
                password_hash=get_password_hash("test1234")
            )
            db.add(usuario)
            db.commit()
        
        # Crear un pedido (solo si no hay para este usuario)
        if db.query(Pedido).filter(Pedido.user_id == usuario.id).count() == 0:
            # Obtener dos plantas para el pedido
            planta1 = db.query(Planta).filter(Planta.nombre_comun == "Hibisco").first()
            planta2 = db.query(Planta).filter(Planta.nombre_comun == "Algarrobo").first()
            
            if planta1 and planta2:
                # Calcular total
                total = float(planta1.precio) * 2 + float(planta2.precio) * 3
                
                # Crear pedido
                nuevo_pedido = Pedido(
                    user_id=usuario.id,
                    fecha=datetime.now(timezone.utc),
                    estado=EstadoPedido.PENDIENTE,
                    total=total
                )
                db.add(nuevo_pedido)
                db.flush()  # Genera el ID
                
                # Crear detalles
                detalle1 = PedidoDetalle(
                    pedido_id=nuevo_pedido.id,
                    planta_id=planta1.id,
                    cantidad=2,
                    precio_unitario=planta1.precio
                )
                detalle2 = PedidoDetalle(
                    pedido_id=nuevo_pedido.id,
                    planta_id=planta2.id,
                    cantidad=3,
                    precio_unitario=planta2.precio
                )
                db.add_all([detalle1, detalle2])
                
                # Descontar stock
                planta1.stock -= 2
                planta2.stock -= 3
                
                db.commit()        
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()