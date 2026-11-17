from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.dependencies import usuario_actual
from src.schemas.usuario import UsuarioCreate, UsuarioRead
from src.services.usuario import autenticar_usuario, registrar_usuario
from src.exceptions import CredencialesInvalidas, UsuarioInactivo, UsuarioYaExiste
from src.schemas.auth import  Token
from src.models.usuario import Usuario
from src.services.auth import crear_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/registro", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def registro(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario en la base de datos."""
    try:
        usuario = registrar_usuario(db, datos)
        return usuario
    except UsuarioYaExiste as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token de acceso."""
    try:
        usuario = autenticar_usuario(db, form.username, form.password)
        token = crear_token(usuario.id)

        return Token(access_token=token)
    
    except CredencialesInvalidas as e:
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    except UsuarioInactivo as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/me", response_model=UsuarioRead)
def obtener_usuario_actual(usuario: Usuario = Depends(usuario_actual)):
    """Obtiene la información del usuario actualmente autenticado."""
    return usuario
    
