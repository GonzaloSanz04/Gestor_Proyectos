from src.models.usuario import Usuario
from sqlalchemy.orm import Session
from sqlalchemy import select


def obtener_por_username(db: Session, username: str) -> Usuario | None:
    """Obtiene un usuario por su nombre de usuario."""
    return db.scalar(select(Usuario).where(Usuario.username == username))

def obtener_por_email(db: Session, email: str) -> Usuario | None:
    """Obtiene un usuario por su dirección de correo electrónico."""
    return db.scalar(select(Usuario).where(Usuario.email == email))

def crear(db: Session, usuario: Usuario) -> Usuario:
    """Crea un nuevo usuario en la base de datos."""
    db.add(usuario)
    db.flush()
    return usuario