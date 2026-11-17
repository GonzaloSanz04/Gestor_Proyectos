

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

import jwt
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models.usuario import Usuario
from src.repositories.usuario import obtener_por_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def usuario_actual(token : str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    """Obtiene el usuario actual a partir del token de acceso."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        usuario_id = int(payload.get("sub"))
        usuario : Usuario | None = obtener_por_id(db, usuario_id)
        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado", headers={"WWW-Authenticate": "Bearer"})
        elif not usuario.activo:
            raise HTTPException(status_code=403, detail="Usuario inactivo")
        
        return usuario
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido", headers={"WWW-Authenticate": "Bearer"})
    except TypeError:
        raise HTTPException(status_code=401, detail="Payload del token inválido", headers={"WWW-Authenticate": "Bearer"})
    except ValueError:
        raise HTTPException(status_code=401, detail="ID de usuario inválido en el token", headers={"WWW-Authenticate": "Bearer"})