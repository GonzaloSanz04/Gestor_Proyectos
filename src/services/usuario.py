

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.exceptions import UsuarioYaExiste
from src.models.usuario import Usuario
from src.repositories.usuario import obtener_por_email, obtener_por_username, crear
from src.schemas.usuario import UsuarioCreate
from src.services.auth import hashear_password


def registrar_usuario(db: Session, datos: UsuarioCreate) -> Usuario:
    """Registra un nuevo usuario en la base de datos."""

    email_lower = datos.email.lower()
    username_lower = datos.username.lower()

    if obtener_por_email(db, email_lower):
        raise UsuarioYaExiste("El correo electrónico ya está en uso")
    elif obtener_por_username(db, username_lower):
        raise UsuarioYaExiste("El nombre de usuario ya está en uso")

    password_hashed = hashear_password(datos.password)
    
    usuario = Usuario(
        username=username_lower,
        nombre=datos.nombre,
        apellidos=datos.apellidos,
        email=email_lower,
        password_hash=password_hashed,
        telefono=datos.telefono,
        activo=True
    )
    try:
        crear(db, usuario)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise UsuarioYaExiste("El usuario ya existe en la base de datos") from e
    return usuario