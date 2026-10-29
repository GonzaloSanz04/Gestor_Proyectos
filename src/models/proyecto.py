from datetime import datetime
from src.database import Base
from src.enums import Estado
from sqlalchemy import DateTime, Enum, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column 

from src.models.utils import ahora



class Proyecto(Base):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(primary_key=True)
    creador_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="RESTRICT"))
    titulo: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(255))
    estado: Mapped[Estado] = mapped_column(Enum(Estado), default=Estado.PLANIFICADO)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora)
    fecha_modificacion: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=ahora, onupdate=ahora)
