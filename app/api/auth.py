from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["Usuarios"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario con email y contraseña. La contraseña se hashea automáticamente",
    responses={
        400: {"description": "El email ya está registrado"}
    }
)
def register_user(usuario: UserCreate, db: Session = Depends(get_db)):
    existe_usuario = db.query(User).filter(User.email == usuario.email).first()

    if existe_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    hashed_password = get_password_hash(usuario.password)

    nuevo_usuario = User(
        nombre=usuario.nombre,
        email=usuario.email,
        password_hash=hashed_password
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.post(
    "/login",
    response_model=Token,
    summary="Inicio de sesión de usuario",
    description="Valida las credenciales y retorna un Bearer Token JWT",
    responses={
        401: {"description": "Email o contraseña no válidos"}
    }
)
def login(usuario: UserLogin, db: Session = Depends(get_db)):
    usuario_db = db.query(User).filter(User.email == usuario.email).first()

    if not usuario_db or not verify_password(usuario.password, str(usuario_db.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña no válidos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token = create_access_token(data={"sub": usuario_db.email})
    return {"access_token": access_token, "token_type": "bearer"}