
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from sqlalchemy import DateTime, ForeignKey

from src.models.utils import ahora


class AsignacionTarea(Base):
    __tablename__ = "asignaciones_tarea"

    tarea_id: Mapped[int] = mapped_column(ForeignKey("tareas.id", ondelete="CASCADE"), unique=True, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    fecha_asignacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    asignado_por: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))