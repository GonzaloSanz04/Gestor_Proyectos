
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.enums import Estado, Prioridad
from sqlalchemy import DateTime, String, Enum, ForeignKey

from src.models.utils import ahora


class Tarea(Base):
    __tablename__ = "tareas"

    id: Mapped[int] = mapped_column(primary_key=True)
    creador_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    user_story_id: Mapped[int] = mapped_column(ForeignKey("user_stories.id", ondelete="CASCADE"))
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[Estado] = mapped_column(Enum(Estado), default=Estado.PLANIFICADO)
    prioridad: Mapped[Prioridad] = mapped_column(Enum(Prioridad))
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora, onupdate=ahora)
    fecha_limite: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)