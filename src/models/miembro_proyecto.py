from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.enums import RolProyecto

from src.models.utils import ahora
from src.database import Base


class MiembroProyecto(Base):
    __tablename__ = "miembros_proyecto"

    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id"), primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    fecha_union: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    rol: Mapped[RolProyecto] = mapped_column(Enum(RolProyecto), default=RolProyecto.USUARIO)