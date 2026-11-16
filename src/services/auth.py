from datetime import UTC, datetime, timedelta

from src.config import settings

import jwt

from pwdlib import PasswordHash

hash = PasswordHash.recommended()

def hashear_password(password: str) -> str:
    """Hashea la contraseña usando pwdlib."""
    return hash.hash(password)

def verificar_password(password: str, hashed: str) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return hash.verify(password, hashed)

def crear_token(usuario_id: int) -> str:
    """Crea un token JWT para el usuario."""
    caducidad = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(usuario_id),
        "exp": caducidad
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)