
from pwdlib import PasswordHash
hash = PasswordHash.recommended()

def hashear_password(password: str) -> str:
    """Hashea la contraseña usando pwdlib."""
    return hash.hash(password)

def verificar_password(password: str, hashed: str) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return hash.verify(password, hashed)