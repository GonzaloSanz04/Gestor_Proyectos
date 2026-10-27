from enum import StrEnum

class Estado(StrEnum):
    PLANIFICADO = "PLANIFICADO"
    EN_CURSO = "EN_CURSO"
    CERRADO = "CERRADO"

class Prioridad(StrEnum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"

class RolGlobal(StrEnum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"

class RolProyecto(StrEnum):
    USUARIO = "USUARIO"
    EDITOR = "EDITOR"
