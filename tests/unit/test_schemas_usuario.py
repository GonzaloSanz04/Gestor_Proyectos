from pydantic import ValidationError
import pytest

from src.schemas.usuario import UsuarioCreate

BASE = {"username": "usuario1", "nombre": "Juan", "apellidos": "Pérez", "email": "juan@example.com", "password": "password123", "telefono": "123456789"}

@pytest.mark.parametrize(
    "campo, valor",
    [
        pytest.param("username", "us", id="invalid_username_too_short"),
        pytest.param("username", "u" * 51, id="invalid_username_too_long"),
        pytest.param("username", "usuario 1", id="invalid_username_with_space"),
        pytest.param("username", "usuario@1", id="invalid_username_with_special_characters"),
        pytest.param("nombre", "J", id="invalid_nombre_too_short"),
        pytest.param("nombre", "J" * 101, id="invalid_nombre_too_long"),
        pytest.param("apellidos", "P", id="invalid_apellidos_too_short"),
        pytest.param("apellidos", "P" * 101, id="invalid_apellidos_too_long"),
        pytest.param("email", "invalid_email", id="invalid_email_format"),
        pytest.param("email", "e" * 101 + "@example.com", id="invalid_email_too_long"),
        pytest.param("password", "pass", id="invalid_password_too_short"),
        pytest.param("password", "p" * 73, id="invalid_password_too_long"),
        pytest.param("telefono", "1" * 21, id="invalid_telefono_too_long"),
    ],
)


def test_usuario_create_validation(campo, valor):
    with pytest.raises(ValidationError) as exc:
        UsuarioCreate(**{**BASE, campo: valor})
    assert campo in [e["loc"][0] for e in exc.value.errors()]

def test_usuario_create_valid():
    usuario = UsuarioCreate(**BASE)
    assert usuario.username == BASE["username"]
    assert usuario.nombre == BASE["nombre"]
    assert usuario.apellidos == BASE["apellidos"]
    assert usuario.email == BASE["email"]
    assert usuario.password == BASE["password"]
    assert usuario.telefono == BASE["telefono"]

def test_usuario_create_telefono_none():
    data = {**BASE, "telefono": None}
    usuario = UsuarioCreate(**data)
    assert usuario.telefono is None