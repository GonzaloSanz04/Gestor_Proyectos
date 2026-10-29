from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.usuario import UsuarioCreate, UsuarioRead
from src.services.usuario import registrar_usuario
from src.exceptions import UsuarioYaExiste

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
