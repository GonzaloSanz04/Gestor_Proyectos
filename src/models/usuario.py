from datetime import UTC, datetime
from enum import Enum
from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.enums import RolGlobal

def ahora() -> datetime:
    return datetime.now(UTC)

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    telefono: Mapped[str | None] = mapped_column(String(20), nullable=True, unique=True)
    rol: Mapped[RolGlobal] = mapped_column(Enum(RolGlobal), default=RolGlobal.USUARIO)
    activo: Mapped[bool] = mapped_column(default=True)
    fecha_alta: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora, onupdate=ahora)